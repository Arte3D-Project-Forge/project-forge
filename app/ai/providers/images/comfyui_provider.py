import json
import os
import sys
import urllib.request
import urllib.parse

from datetime import datetime

from app.ai.providers.images.image_provider import ImageProvider
from app.core.config_manager import ConfigManager
from app.services.background_remover import remove_background


class ComfyUIProvider(ImageProvider):

    def __init__(self):
        config = ConfigManager()
        comfyui_cfg = config.config.get("comfyui", {})
        generation_cfg = config.config.get("generation", {})

        self.base_url = comfyui_cfg.get(
            "server_url",
            os.getenv("COMFYUI_SERVER_URL", "http://127.0.0.1:8188")
        ).rstrip("/")

        self.default_model_name = comfyui_cfg.get("default_model", "")
        self.steps = comfyui_cfg.get("steps", 28)
        self.cfg = comfyui_cfg.get("cfg", 7)
        self.sampler = comfyui_cfg.get("sampler", "dpmpp_2m")
        self.scheduler = comfyui_cfg.get("scheduler", "karras")
        self.workflow_path = comfyui_cfg.get(
            "workflow",
            "config/workflows/comfyui_sprite_workflow.json"
        )
        self.upscale_workflow_path = comfyui_cfg.get(
            "upscale_workflow",
            "config/workflows/comfyui_sprite_upscale_workflow.json"
        )
        self.upscale_model = comfyui_cfg.get(
            "upscale_model",
            "RealESRGAN_x4plus.pth"
        )
        self.positive_suffix = comfyui_cfg.get(
            "positive_suffix",
            "game sprite, clean edges, single subject, centered, full body, sharp focus"
        )
        self.negative_prompt = comfyui_cfg.get(
            "negative_prompt",
            "blurry, low quality, deformed, distorted, ugly, bad anatomy, "
            "watermark, text, logo, signature, realistic photo, 3d render, "
            "multiple subjects, cropped, out of frame, extra limbs"
        )

        self.transparent_background = generation_cfg.get(
            "transparent_background", True
        )
        self.style_suffix = generation_cfg.get(
            "style_suffix",
            "pixel art, game asset, 16bit, rpg style, high quality, detailed, sharp pixels"
        )

        resolution = generation_cfg.get(
            "default_resolution", "512x512"
        ).lower().split("x")
        self.width = int(resolution[0])
        self.height = int(resolution[1])

    def generate(
        self,
        prompt,
        filename,
        output_path
    ):
        try:
            os.makedirs(
                output_path,
                exist_ok=True
            )

            self.check_server()

            workflow = self.build_workflow(prompt, use_upscale=True)
            prompt_id, node_errors = self.queue_prompt(workflow)

            if node_errors:
                self._log_workflow_error(node_errors)

                workflow = self.build_workflow(
                    prompt,
                    use_upscale=False
                )
                prompt_id, node_errors = self.queue_prompt(workflow)

                if node_errors:
                    raise RuntimeError(
                        "Workflow invalido no ComfyUI: "
                        f"{node_errors}"
                    )

            images = self.wait_for_images(prompt_id)

            saved_files = self.save_images(
                images,
                filename,
                output_path
            )

            return {
                "status": "generated",
                "provider": "comfyui",
                "server": self.base_url,
                "files": saved_files,
                "created_at":
                    datetime.now().isoformat()
            }

        except Exception as error:
            return {
                "status": "error",
                "provider": "comfyui",
                "message": str(error)
            }

    def check_server(self):
        try:
            req = urllib.request.Request(
                f"{self.base_url}/system_stats"
            )
            urllib.request.urlopen(
                req,
                timeout=10
            )
        except Exception as exc:
            raise ConnectionError(
                f"ComfyUI não está acessível em {self.base_url}. "
                f"Se estiver usando Colab, execute o notebook e "
                f"cole a URL do túnel no campo ComfyUI do Forge. "
                f"Se for local, inicie o ComfyUI primeiro. "
                f"Detalhes: {exc}"
            )

    def _load_workflow_template(self, path=None):
        resolved = path or self.workflow_path
        if not os.path.exists(resolved):
            candidates = []

            if getattr(sys, "frozen", False):
                candidates.append(
                    os.path.join(
                        getattr(sys, "_MEIPASS", ""),
                        resolved
                    )
                )

            candidates.append(
                os.path.join(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.dirname(
                                os.path.dirname(
                                    os.path.abspath(__file__)
                                )
                            )
                        )
                    ),
                    resolved
                )
            )

            for candidate in candidates:
                if os.path.exists(candidate):
                    resolved = candidate
                    break

        with open(resolved, "r", encoding="utf-8") as f:
            return json.load(f)

    def build_workflow(self, prompt_text, use_upscale=True):
        template_path = (
            self.upscale_workflow_path
            if use_upscale
            else self.workflow_path
        )
        workflow = self._load_workflow_template(template_path)
        workflow.pop("description", None)

        positive = self.build_positive_prompt(prompt_text)
        seed = self.build_seed(prompt_text)
        model_name = self.find_model()

        values = {
            "__CHECKPOINT__": model_name,
            "__PROMPT__": positive,
            "__NEGATIVE__": self.negative_prompt,
            "__WIDTH__": self.width,
            "__HEIGHT__": self.height,
            "__SEED__": seed,
            "__STEPS__": self.steps,
            "__CFG__": self.cfg,
            "__SAMPLER__": self.sampler,
            "__SCHEDULER__": self.scheduler,
            "__FILENAME_PREFIX__": "forge_output"
        }

        if use_upscale:
            values["__UPSCALE_MODEL__"] = self.upscale_model

        return self._fill_template(workflow, values)

    def build_positive_prompt(self, prompt_text):
        parts = [prompt_text.strip()]

        if self.style_suffix and self.style_suffix not in prompt_text:
            parts.append(self.style_suffix)

        if self.positive_suffix and self.positive_suffix not in prompt_text:
            parts.append(self.positive_suffix)

        return ", ".join(parts)

    def build_seed(self, prompt_text):
        return abs(hash(prompt_text)) % (2**32)

    def _fill_template(self, node, values):
        if isinstance(node, dict):
            return {
                key: self._fill_template(value, values)
                for key, value in node.items()
            }

        if isinstance(node, list):
            return [
                self._fill_template(item, values)
                for item in node
            ]

        if isinstance(node, str) and node in values:
            return values[node]

        if isinstance(node, str) and "__" in node:
            for key, value in values.items():
                node = node.replace(key, str(value))
            return node

        return node

    def find_model(self):
        if self.default_model_name:
            return self.default_model_name

        for base in [
            os.path.join(
                os.path.dirname(__file__),
                "..", "..", "..", "..",
                "ComfyUI_windows_portable_amd",
                "ComfyUI_windows_portable",
                "ComfyUI",
                "models",
                "checkpoints"
            ),
            os.path.expanduser(
                "~/ComfyUI_windows_portable_amd/"
                "ComfyUI_windows_portable/ComfyUI/"
                "models/checkpoints"
            ),
            os.path.expanduser(
                "~/ComfyUI/models/checkpoints"
            )
        ]:
            resolved = os.path.abspath(base)
            if os.path.exists(resolved):
                models = [
                    f for f in os.listdir(resolved)
                    if f.endswith((".safetensors", ".ckpt"))
                ]
                if models:
                    return models[0]

        raise FileNotFoundError(
            "Nenhum modelo SD encontrado localmente. "
            "Defina default_model no forge_config.json "
            "ou baixe um .safetensors de civitai.com "
            "e coloque em ComfyUI/models/checkpoints/"
        )

    def queue_prompt(self, workflow):
        data = json.dumps({
            "prompt": workflow
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{self.base_url}/prompt",
            data=data,
            headers={
                "Content-Type":
                    "application/json"
            }
        )

        response = urllib.request.urlopen(req)
        result = json.loads(
            response.read().decode("utf-8")
        )

        node_errors = result.get("node_errors") or {}
        prompt_id = result.get("prompt_id")

        if not prompt_id:
            raise RuntimeError(
                "ComfyUI recusou o workflow: "
                f"{node_errors}"
            )

        return prompt_id, node_errors

    def _log_workflow_error(self, node_errors):
        try:
            summary = []
            for node_id, err in node_errors.items():
                summary.append(
                    f"{node_id}: {err.get('errors', [])}"
                )
            self.logger.warning(
                "ComfyUI workflow com erro, "
                f"usando workflow basico: "
                f"{'; '.join(summary)}"
            )
        except Exception:
            pass

    def wait_for_images(
        self,
        prompt_id,
        timeout=600
    ):
        import time

        start = time.time()

        while True:
            if time.time() - start > timeout:
                raise TimeoutError(
                    "ComfyUI demorou demais "
                    "para gerar a imagem."
                )

            req = urllib.request.Request(
                f"{self.base_url}/history/"
                f"{prompt_id}"
            )

            response = urllib.request.urlopen(
                req
            )

            history = json.loads(
                response.read().decode("utf-8")
            )

            if prompt_id in history:
                outputs = (
                    history[prompt_id]
                    .get("outputs", {})
                )

                images = []
                for node_id in outputs:
                    node_images = (
                        outputs[node_id]
                        .get("images", [])
                    )
                    images.extend(node_images)

                if images:
                    return images

            time.sleep(1)

    def save_images(
        self,
        images,
        filename,
        output_path
    ):
        saved = []

        for i, image_info in enumerate(images):
            subfolder = image_info.get(
                "subfolder", ""
            )
            image_filename = (
                image_info["filename"]
            )
            image_type = image_info.get(
                "type", "output"
            )

            params = urllib.parse.urlencode({
                "filename": image_filename,
                "subfolder": subfolder,
                "type": image_type
            })

            req = urllib.request.Request(
                f"{self.base_url}/view?{params}"
            )

            response = urllib.request.urlopen(req)
            image_data = response.read()

            ext = os.path.splitext(
                image_filename
            )[1] or ".png"

            save_name = (
                f"{filename}"
                f"_{i + 1}"
                f"{ext}"
            )

            save_path = os.path.join(
                output_path,
                save_name
            )

            with open(save_path, "wb") as f:
                f.write(image_data)

            saved.append(save_path)

            if self.transparent_background:
                transparent = remove_background(save_path)
                if transparent:
                    if transparent != save_path:
                        os.replace(transparent, save_path)
                        saved[-1] = save_path

        return saved
