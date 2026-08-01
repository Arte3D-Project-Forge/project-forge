import os
import time
import base64
import httpx

from datetime import datetime

from app.ai.providers.images.image_provider import ImageProvider


class StableHordeProvider(ImageProvider):
    """
    Stable Horde (AI Horde) - rede distribuida e GRATUITA de GPUs
    comunitarias. Sem custo, sem login obrigatorio (anonimo = fila
    mais lenta). Alternativa ao Colab/ComfyUI para o projeto Aetherva.
    """

    API_BASE = "https://aihorde.net/api/v2"
    DEFAULT_MODEL = "AIO Pixel Art"

    def __init__(self):
        from app.core.config_manager import ConfigManager

        config = ConfigManager()
        generation = config.config.get("generation", {})
        resolution = generation.get(
            "default_resolution", "1024x1024"
        ).lower().split("x")
        horde_cfg = config.config.get("stablehorde", {})

        self.model = horde_cfg.get("model", "AIO Pixel Art")
        self.width = int(resolution[0])
        self.height = int(resolution[1])
        self.timeout = 600
        self.poll_interval = 4
        self.max_poll_attempts = 120
        self.client = httpx.Client(
            timeout=httpx.Timeout(self.timeout),
            follow_redirects=True,
            verify=False
        )
        self.api_key = (
            horde_cfg.get("api_key", "")
            or os.environ.get("AI_HORDE_API_KEY", "")
            or "0000000000"
        )

        studio_cfg = config.config.get("studio_pro", {})
        self.master_prompt = studio_cfg.get(
            "master_prompt",
            "professional indie RPG sprite, masterpiece, best quality, "
            "unified cohesive pixel art style inspired by Ragnarok Online, "
            "Zelda Link to the Past, Final Fantasy VI and Digimon, vibrant "
            "harmonious fantasy color palette, clean sharp pixel lines, "
            "perfect subtle dithering, soft cel-shading, consistent art "
            "direction across all assets, transparent background, "
            "game-ready asset"
        )
        self.negative_prompt = studio_cfg.get(
            "negative_prompt",
            "blurry, lowres, deformed, bad anatomy, extra limbs, jpeg "
            "artifacts, different art style, realistic, 3d, photorealistic, "
            "oversaturated, inconsistent lighting"
        )

    def _headers(self):
        return {
            "User-Agent": "ProjectForge/0.1 (https://projectforge.local)",
            "apikey": self.api_key,
        }

    def generate(self, prompt, filename, output_path):
        os.makedirs(output_path, exist_ok=True)

        last_error = "erro desconhecido"

        try:
            job_id = self._submit(prompt)
            if not job_id:
                return {
                    "status": "error",
                    "provider": "stablehorde",
                    "error": "Falha ao submeter job na Stable Horde",
                }

            image_data = self._wait_for_result(job_id, last_error)
            if image_data is None:
                return {
                    "status": "error",
                    "provider": "stablehorde",
                    "error": f"Job nao concluiu ou sem imagem: {last_error}",
                }

            ext = ".png"
            if image_data[:4] == b"\x89PNG":
                ext = ".png"
            elif image_data[:2] == b"\xff\xd8":
                ext = ".jpg"
            elif image_data[:4] == b"RIFF":
                ext = ".webp"

            file_path = os.path.join(output_path, filename + ext)
            with open(file_path, "wb") as f:
                f.write(image_data)

            return {
                "status": "generated",
                "provider": "stablehorde",
                "model": self.model,
                "file": file_path,
                "format": ext,
                "size": len(image_data),
                "attempts": 1,
                "created_at": datetime.now().isoformat()
            }

        except httpx.ConnectError as e:
            last_error = f"Sem conexao com o servidor: {e}"
        except Exception as e:
            last_error = f"{type(e).__name__}: {e}"

        return {
            "status": "error",
            "provider": "stablehorde",
            "error": last_error,
        }

    def _decode_image(self, raw):
        """Decodifica a imagem retornada: base64 puro, data URI ou URL."""
        if raw.startswith("data:image"):
            return base64.b64decode(raw.split(",", 1)[1])
        if raw.startswith("http"):
            resp = self.client.get(raw)
            if resp.status_code == 200 and resp.content:
                return resp.content
            return None
        # base64 puro
        try:
            return base64.b64decode(raw)
        except Exception:
            return None

    def _submit(self, prompt):
        full_prompt = prompt.strip()
        if self.master_prompt and self.master_prompt not in full_prompt:
            full_prompt = f"{full_prompt}, {self.master_prompt}"

        for attempt in range(2):
            if attempt == 1:
                # 1024x1024 anonimo pode exigir kudos; tenta 512x512.
                width, height = 512, 512
            else:
                width, height = self.width, self.height
            payload = {
                "prompt": full_prompt,
                "model": self.model,
                "params": {
                    "width": width,
                    "height": height,
                    "steps": 28,
                    "cfg_scale": 5.5,
                    "sampler_name": "k_euler_a",
                    "negative_prompt": self.negative_prompt,
                },
                "nsfw": False,
                "slow_workers": True,
            }
            response = self.client.post(
                f"{self.API_BASE}/generate/async",
                json=payload,
                headers=self._headers(),
            )
            if response.status_code in (200, 202):
                data = response.json()
                return data.get("id")
            if response.status_code in (400, 403):
                # erro de kudos/validacao: tenta resolucao menor uma vez
                continue
            return None
        return None

    def _wait_for_result(self, job_id, last_error):
        for _ in range(self.max_poll_attempts):
            try:
                response = self.client.get(
                    f"{self.API_BASE}/generate/status/{job_id}",
                    headers=self._headers(),
                )
                if response.status_code != 200:
                    last_error = (
                        f"Status HTTP {response.status_code}"
                    )
                    time.sleep(self.poll_interval)
                    continue

                data = response.json()
                if data.get("done"):
                    generations = data.get("generations", [])
                    if not generations:
                        last_error = "Job terminou sem geracoes"
                        return None
                    raw = generations[0].get("img")
                    if not raw:
                        last_error = "Geracao sem imagem"
                        return None
                    return self._decode_image(raw)

                if data.get("faulted"):
                    last_error = "Job falhou no worker (faulted)"
                    return None

                time.sleep(self.poll_interval)
            except Exception as e:
                last_error = f"{type(e).__name__}: {e}"
                time.sleep(self.poll_interval)

        return None
