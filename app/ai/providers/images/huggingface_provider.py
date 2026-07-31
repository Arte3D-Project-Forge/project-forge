import os
import httpx

from datetime import datetime

from app.ai.providers.images.image_provider import ImageProvider


class HuggingFaceProvider(ImageProvider):

    def __init__(self):
        self.env = None
        try:
            from app.core.env_manager import EnvManager
            self.env = EnvManager()
        except Exception:
            pass

        self.api_token = self._get_token()
        self.model = "black-forest-labs/FLUX.1-schnell"
        self.timeout = 120
        self.max_attempts = 3

        if self.api_token:
            self.client = httpx.Client(
                timeout=httpx.Timeout(self.timeout),
                verify=False,
                headers={"Authorization": f"Bearer {self.api_token}"}
            )
        else:
            self.client = None

    def _get_token(self):
        if self.env:
            token = self.env.get("HF_API_TOKEN")
            if token:
                return token

        try:
            from app.core.config_manager import ConfigManager
            config = ConfigManager()
            token = config.config.get("providers", {}).get(
                "huggingface", {}
            ).get("api_token", "")
            if token:
                return token
        except Exception:
            pass

        return os.getenv("HF_API_TOKEN", "")

    def is_configured(self):
        return self.client is not None and bool(self.api_token)

    def generate(self, prompt, filename, output_path):
        if not self.is_configured():
            return {
                "status": "error",
                "provider": "huggingface",
                "message": (
                    "HuggingFace API token nao configurado. "
                    "Gere um token gratis em: "
                    "https://huggingface.co/settings/tokens"
                )
            }

        os.makedirs(output_path, exist_ok=True)

        last_error = "erro desconhecido"

        for attempt in range(1, self.max_attempts + 1):
            try:
                url = (
                    f"https://api-inference.huggingface.co/"
                    f"models/{self.model}"
                )

                payload = {
                    "inputs": f"{prompt}, pixel art, game sprite, "
                              f"16bit, rpg character, high quality, "
                              f"detailed, sharp pixels, transparent background"
                }

                response = self.client.post(url, json=payload)

                if response.status_code == 503:
                    import time
                    wait = response.json().get("estimated_time", 10)
                    time.sleep(min(wait, 30))
                    response = self.client.post(url, json=payload)

                if response.status_code != 200:
                    error_body = response.text[:200]
                    last_error = (
                        f"API retornou status {response.status_code}: "
                        f"{error_body}"
                    )
                    import time
                    time.sleep(2 * attempt)
                    continue

                content_type = response.headers.get("content-type", "")
                image_data = response.content

                if not image_data:
                    last_error = "API retornou dados vazios"
                    import time
                    time.sleep(2 * attempt)
                    continue

                if "text/html" in content_type or "application/json" in content_type:
                    last_error = f"API retornou JSON/HTML em vez de imagem"
                    import time
                    time.sleep(2 * attempt)
                    continue

                ext = ".png"
                if image_data[:2] == b"\xff\xd8":
                    ext = ".jpg"
                elif image_data[:4] == b"\x89PNG":
                    ext = ".png"
                elif image_data[:4] == b"RIFF":
                    ext = ".webp"

                file_path = os.path.join(output_path, filename + ext)

                with open(file_path, "wb") as f:
                    f.write(image_data)

                return {
                    "status": "generated",
                    "provider": "huggingface",
                    "model": self.model,
                    "file": file_path,
                    "format": ext,
                    "size": len(image_data),
                    "attempts": attempt,
                    "created_at": datetime.now().isoformat()
                }

            except httpx.ConnectError as e:
                last_error = f"Sem conexao (tentativa {attempt}): {e}"
                import time
                time.sleep(2 * attempt)

            except httpx.TimeoutException:
                last_error = f"Timeout (tentativa {attempt})"
                import time
                time.sleep(2 * attempt)

            except Exception as error:
                last_error = f"{error} (tentativa {attempt})"
                import time
                time.sleep(2 * attempt)

        return {
            "status": "error",
            "provider": "huggingface",
            "message": (
                f"Falha apos {self.max_attempts} tentativas. "
                f"Ultimo erro: {last_error}"
            )
        }
