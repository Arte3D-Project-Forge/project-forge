from app.ai.providers.base_provider import BaseProvider


class ComfyUIProvider(BaseProvider):

    def get_name(self):
        return "ComfyUI"

    def generate_text(self, prompt):
        return "ComfyUI text generation not implemented yet."

    def generate_json(self, prompt):
        return {"provider": "comfyui", "status": "pending"}

    def generate_image(self, prompt, output_path):
        return {"provider": "comfyui", "status": "pending", "message": "Use the Image Provider instead."}
