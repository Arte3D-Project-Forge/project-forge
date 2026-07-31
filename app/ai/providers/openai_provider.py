from app.ai.providers.base_provider import BaseProvider
from app.core.env_manager import EnvManager


class OpenAIProvider(BaseProvider):

    def __init__(self):
        self.env = EnvManager()
        self.api_key = self.env.get("OPENAI_API_KEY")
        self.client = None

    def get_name(self):
        return "OpenAI"

    def generate_text(self, prompt):
        return "OpenAI text generation not implemented yet."

    def generate_json(self, prompt):
        return {"provider": "openai", "status": "pending"}

    def generate_image(self, prompt, output_path):
        return {"provider": "openai", "status": "pending"}
