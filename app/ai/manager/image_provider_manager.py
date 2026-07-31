from app.core.config_manager import ConfigManager

from app.ai.providers.images.mock_image_provider import MockImageProvider
from app.ai.providers.images.openai_image_provider import OpenAIImageProvider
from app.ai.providers.images.comfyui_provider import ComfyUIProvider
from app.ai.providers.images.pollinations_provider import PollinationsProvider
from app.ai.providers.images.huggingface_provider import HuggingFaceProvider


class ImageProviderManager:

    def __init__(self):
        self.config = ConfigManager()
        self.provider_name = self.config.get_image_provider()
        self.primary_provider = self.load_provider(self.provider_name)
        self.fallback = MockImageProvider()

    def load_provider(self, name):
        if name == "openai":
            return OpenAIImageProvider()
        if name == "comfyui":
            return ComfyUIProvider()
        if name == "pollinations":
            return PollinationsProvider()
        if name == "huggingface":
            return HuggingFaceProvider()
        if name == "mock":
            return MockImageProvider()
        return PollinationsProvider()

    def comfyui_available(self, timeout=3):
        try:
            import urllib.request

            comfyui_cfg = self.config.config.get("comfyui", {})
            base_url = comfyui_cfg.get(
                "server_url",
                "http://127.0.0.1:8188"
            ).rstrip("/")

            req = urllib.request.Request(
                f"{base_url}/system_stats"
            )
            urllib.request.urlopen(req, timeout=timeout)
            return True
        except Exception:
            return False

    def _comfyui_explicit(self):
        server_url = (
            self.config.config.get("comfyui", {})
            .get("server_url", "")
            .rstrip("/")
        )

        if self.provider_name == "comfyui":
            return True

        if not server_url:
            return False

        return (
            "127.0.0.1" not in server_url
            and "localhost" not in server_url
        )

    def generate(self, prompt, filename, output_path):
        comfyui_explicit = self._comfyui_explicit()

        if comfyui_explicit or self.comfyui_available():
            comfy_result = self.load_provider("comfyui").generate(
                prompt, filename, output_path
            )

            if comfy_result.get("status") == "generated":
                self._log(
                    "ComfyUI usado em "
                    f"{self.config.get('comfyui', 'server_url')}"
                )
                return comfy_result

            if comfyui_explicit:
                return comfy_result

        result = self.primary_provider.generate(
            prompt, filename, output_path
        )

        if result.get("status") == "error":
            import os
            import json

            providers_to_try = ["pollinations", "huggingface"]
            if self.provider_name not in providers_to_try:
                providers_to_try.insert(0, self.provider_name)

            for name in providers_to_try:
                if name == self.provider_name:
                    continue

                try:
                    provider = self.load_provider(name)
                    if hasattr(provider, "is_configured") and not provider.is_configured():
                        continue
                except Exception:
                    continue

                result2 = provider.generate(
                    prompt, filename, output_path
                )

                if result2.get("status") == "generated":
                    self._log_fallback(
                        self.provider_name, name, prompt
                    )
                    return result2

            return {
                "status": "error",
                "provider": self.provider_name,
                "message": (
                    f"Falha em todos os providers. "
                    f"Ultimo erro: {result.get('message', 'desconhecido')}"
                )
            }

        return result

    def _log(self, message):
        try:
            import os

            log_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "fallback.log"
            )
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"[info] {message}\n")
        except Exception:
            pass

    def _log_fallback(self, failed, used, prompt):
        try:
            log_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "fallback.log"
            )
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(
                    f"[{used}] Provider '{failed}' falhou. "
                    f"Fallback para '{used}'. Prompt: {prompt[:50]}\n"
                )
        except Exception:
            pass
