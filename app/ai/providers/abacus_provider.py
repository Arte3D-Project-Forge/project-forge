from app.ai.providers.base_provider import BaseProvider


class AbacusProvider(BaseProvider):

    def get_name(self):
        return "Abacus AI"

    def generate_text(self, prompt):
        return "Abacus AI not implemented yet."

    def generate_json(self, prompt):
        return {"provider": "abacus", "status": "pending"}

    def generate_image(self, prompt, output_path):
        return {"provider": "abacus", "status": "pending"}
