import os
import time
import httpx

from datetime import datetime

from app.ai.providers.images.image_provider import ImageProvider


class PollinationsProvider(ImageProvider):

    def __init__(self):
        from app.core.config_manager import ConfigManager

        config = ConfigManager()
        generation = config.config.get("generation", {})
        resolution = generation.get(
            "default_resolution", "512x512"
        ).lower().split("x")

        self.model = "flux"
        self.timeout = 180
        self.width = int(resolution[0])
        self.height = int(resolution[1])
        self.max_attempts = 3
        self.client = httpx.Client(
            timeout=httpx.Timeout(self.timeout),
            follow_redirects=True,
            verify=False
        )

    def generate(self, prompt, filename, output_path):
        os.makedirs(output_path, exist_ok=True)

        last_error = "erro desconhecido"

        for attempt in range(1, self.max_attempts + 1):
            try:
                url = self._build_url(prompt, attempt)

                response = self.client.get(url)

                if response.status_code != 200:
                    last_error = (
                        f"API retornou status {response.status_code} "
                        f"(tentativa {attempt}/{self.max_attempts})"
                    )
                    time.sleep(2 * attempt)
                    continue

                content_type = response.headers.get("content-type", "")
                image_data = response.content

                if not image_data:
                    last_error = (
                        f"API retornou imagem vazia "
                        f"(tentativa {attempt}/{self.max_attempts})"
                    )
                    time.sleep(2 * attempt)
                    continue

                if "text/html" in content_type:
                    last_error = (
                        f"API retornou HTML em vez de imagem. "
                        f"Resposta: {image_data[:200].decode('utf-8', errors='replace')}"
                    )
                    time.sleep(2 * attempt)
                    continue

                ext = ".png"
                if image_data[:2] == b"\xff\xd8":
                    ext = ".jpg"
                elif image_data[:4] == b"\x89PNG":
                    ext = ".png"
                elif image_data[:6] in (b"GIF87a", b"GIF89a"):
                    ext = ".gif"
                elif image_data[:4] == b"RIFF":
                    ext = ".webp"

                file_path = os.path.join(output_path, filename + ext)

                with open(file_path, "wb") as f:
                    f.write(image_data)

                return {
                    "status": "generated",
                    "provider": "pollinations",
                    "model": self.model,
                    "file": file_path,
                    "format": ext,
                    "size": len(image_data),
                    "attempts": attempt,
                    "created_at": datetime.now().isoformat()
                }

            except httpx.ConnectError as e:
                last_error = f"Sem conexao com o servidor (tentativa {attempt}): {e}"
                self._log_error(last_error)
                time.sleep(2 * attempt)

            except httpx.TimeoutException:
                last_error = f"Servidor demorou demais (tentativa {attempt})"
                self._log_error(last_error)
                time.sleep(2 * attempt)

            except Exception as error:
                last_error = f"{error} (tentativa {attempt})"
                self._log_error(last_error)
                time.sleep(2 * attempt)

        return {
            "status": "error",
            "provider": "pollinations",
            "message": (
                f"Nao foi possivel gerar a imagem apos "
                f"{self.max_attempts} tentativas. Ultimo erro: {last_error}"
            )
        }

    def _build_url(self, prompt, attempt=1):
        import urllib.parse
        encoded = urllib.parse.quote(prompt)
        seed = (abs(hash(prompt)) + attempt * 12345) % (2**16)
        params = urllib.parse.urlencode({
            "width": self.width,
            "height": self.height,
            "model": self.model,
            "nologo": "true",
            "enhance": "true",
            "seed": seed
        })
        return (
            f"https://image.pollinations.ai/prompt/"
            f"{encoded}?{params}"
        )

    def _log_error(self, msg):
        try:
            log_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "pollinations_errors.log"
            )
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().isoformat()}] {msg}\n")
        except Exception:
            pass
