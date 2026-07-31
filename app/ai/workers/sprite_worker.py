import os
import json

from datetime import datetime

from app.ai.manager.image_provider_manager import ImageProviderManager


class SpriteWorker:

    def __init__(self):
        self.image_manager = ImageProviderManager()

    def run(self, job, package_path):
        asset_name = self.create_asset_name(job.request)
        prompt = job.request
        return self.generate(
            project=job.project,
            asset_name=asset_name,
            prompt=prompt
        )

    def create_asset_name(self, request):
        words = request.lower().split()
        return "_".join(words[:3])

    def generate(self, project, asset_name, prompt, animations=None):
        if animations is None:
            animations = ["idle"]

        output_path = os.path.join(
            project["path"],
            "sprites",
            asset_name
        )
        os.makedirs(output_path, exist_ok=True)

        generated_files = []

        for animation in animations:
            animation_path = os.path.join(output_path, animation)
            os.makedirs(animation_path, exist_ok=True)

            filename = f"{asset_name}_{animation}_001"

            result = self.image_manager.generate(
                prompt=f"{prompt}\n\nAnimation: {animation}",
                filename=filename,
                output_path=animation_path
            )

            if result.get("status") == "error":
                raise Exception(
                    f"Falha ao gerar sprite '{filename}': "
                    f"{result.get('message', 'erro desconhecido')}"
                )

            result = self._apply_transparency(result)

            generated_files.append(result)

        metadata = {
            "asset": asset_name,
            "prompt": prompt,
            "animations": animations,
            "files": generated_files,
            "created_at": datetime.now().isoformat()
        }

        meta_path = os.path.join(output_path, "sprite_generation.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)

        return output_path

    def _apply_transparency(self, result):
        if result.get("status") != "generated":
            return result

        from app.core.config_manager import ConfigManager

        generation = ConfigManager().config.get("generation", {})
        if not generation.get("transparent_background", True):
            return result

        files = result.get("files")
        if files:
            updated = []
            for entry in files:
                if isinstance(entry, str):
                    entry = {"file": entry, "status": "generated"}
                if entry.get("file"):
                    processed = self._make_transparent(
                        entry["file"]
                    )
                    entry["file"] = self._pixelate(processed)
                updated.append(entry)
            result["files"] = updated
            return result

        file_path = result.get("file")
        if file_path:
            processed = self._make_transparent(file_path)
            result["file"] = self._pixelate(processed)

        return result

    def _pixelate(self, path):
        try:
            from app.core.config_manager import ConfigManager

            generation = ConfigManager().config.get("generation", {})
            if not generation.get("pixel_art", True):
                return path

            from PIL import Image

            image = Image.open(path).convert("RGBA")
            width, height = image.size

            max_side = 1024
            if max(width, height) > max_side:
                scale = max_side / max(width, height)
                image = image.resize(
                    (
                        max(1, round(width * scale)),
                        max(1, round(height * scale)),
                    ),
                    Image.LANCZOS,
                )
                width, height = image.size

            grid = max(48, min(192, width // 8))

            small = image.resize(
                (grid, grid),
                Image.LANCZOS
            )
            pixelated = small.resize(
                (width, height),
                Image.NEAREST
            )

            palette_image = pixelated.convert("RGB").quantize(
                colors=256,
                method=Image.MEDIANCUT,
            ).convert("RGBA")

            palette_image.putalpha(pixelated.getchannel("A"))
            palette_image.save(path, "PNG")
            return path
        except Exception:
            return path

    def _make_transparent(self, path):
        try:
            from PIL import Image

            image = Image.open(path)
            if image.mode == "RGBA":
                return path
        except Exception:
            return path

        from app.services.background_remover import remove_background

        result = remove_background(path)
        return result if result else path
