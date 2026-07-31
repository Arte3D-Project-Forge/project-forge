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
