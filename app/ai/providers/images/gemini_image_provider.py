import os
import base64
import httpx

from datetime import datetime

from app.ai.providers.images.image_provider import ImageProvider


class GeminiImageProvider(ImageProvider):
    """
    Gemini API (Google AI Studio) - geracao de imagens NATIVAS gratis.

    Usa o modelo "Nano Banana" (gemini-2.5-flash-image), disponivel
    no tier gratuito da Gemini API (~10 imagens/dia).

    Vantagens:
    - Gratis (sem GPU, sem tunel, sem Colab)
    - Chamada REST direta do Forge
    - Retorna imagem como base64 (sem URL para decodificar)

    Para ativar:
    1. Crie chave gratis em https://aistudio.google.com/apikey
    2. Coloque em Configuracoes > Gemini API key
       ou em config/.env:  GEMINI_API_KEY=...
    """

    API_BASE = "https://generativelanguage.googleapis.com/v1beta"
    DEFAULT_MODEL = "gemini-2.5-flash-image"

    def __init__(self):
        from app.core.config_manager import ConfigManager
        from app.core.env_manager import EnvManager

        EnvManager().load()
        config = ConfigManager()
        cfg = config.config.get("gemini", {})

        self.api_key = (
            cfg.get("api_key", "")
            or os.environ.get("GEMINI_API_KEY", "")
        )
        self.model = cfg.get("model", self.DEFAULT_MODEL)
        self.steps = int(cfg.get("steps", 28) or 28)
        self.timeout = 300
        self.client = httpx.Client(
            timeout=httpx.Timeout(self.timeout),
            follow_redirects=True,
            verify=False,
        )

    def is_configured(self):
        return bool(self.api_key)

    def _headers(self):
        return {"Content-Type": "application/json"}

    def _config_url(self):
        return f"{self.API_BASE}/models/{self.model}:generateContent?key={self.api_key}"

    def generate(self, prompt, filename, output_path):
        if not self.is_configured():
            return {
                "status": "error",
                "provider": "gemini",
                "error": (
                    "Gemini sem API key. Crie a chave gratuita em "
                    "aistudio.google.com/apikey e configure em "
                    "Configuracoes ou config/.env (GEMINI_API_KEY)."
                ),
            }

        os.makedirs(output_path, exist_ok=True)
        last_error = "erro desconhecido"

        try:
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": self._build_image_prompt(prompt)},
                        ]
                    }
                ],
                "generationConfig": {
                    "imageConfig": {
                        "aspectRatio": "SQUARE",
                        "imageSize": "1K",
                    }
                },
            }

            response = self.client.post(
                self._config_url(),
                json=payload,
                headers=self._headers(),
            )

            if response.status_code != 200:
                return {
                    "status": "error",
                    "provider": "gemini",
                    "error": (
                        f"Gemini HTTP {response.status_code}: "
                        f"{self._error_message(response)}"
                    ),
                }

            data = response.json()
            image_data, mime = self._extract_image(data)

            if not image_data:
                return {
                    "status": "error",
                    "provider": "gemini",
                    "error": "Gemini retornou sem imagem no corpo.",
                }

            ext = self._mime_to_ext(mime)
            file_path = os.path.join(output_path, filename + ext)
            with open(file_path, "wb") as f:
                f.write(image_data)

            return {
                "status": "generated",
                "provider": "gemini",
                "model": self.model,
                "file": file_path,
                "format": ext,
                "size": len(image_data),
                "created_at": datetime.now().isoformat(),
            }

        except httpx.ConnectError as e:
            last_error = f"Sem conexao com o servidor: {e}"
        except Exception as e:
            last_error = f"{type(e).__name__}: {e}"

        return {
            "status": "error",
            "provider": "gemini",
            "error": last_error,
        }

    def _build_image_prompt(self, prompt):
        from app.core.config_manager import ConfigManager

        config = ConfigManager()
        studio = config.config.get("studio_pro", {})
        master = studio.get(
            "master_prompt",
            "professional indie RPG sprite, masterpiece, best quality, "
            "unified cohesive pixel art style, vibrant harmonious fantasy "
            "color palette, clean sharp pixel lines, perfect subtle "
            "dithering, soft cel-shading, transparent background, "
            "game-ready asset"
        )

        text = prompt.strip()
        if master and master not in text:
            text = f"{text}, {master}"

        text += (
            ", pure pixel art, sharp crisp pixels, grid aligned, "
            "no anti-aliasing, no gradients, limited color palette, "
            "game sprite"
        )
        return text

    def _extract_image(self, data):
        """Extrai a imagem inline (base64) do retorno do Gemini."""
        try:
            candidates = data.get("candidates", [])
            if not candidates:
                return None, None

            parts = candidates[0].get("content", {}).get("parts", [])
            for part in parts:
                inline = part.get("inlineData")
                if inline and inline.get("data"):
                    mime = inline.get("mimeType", "image/png")
                    raw = base64.b64decode(inline["data"])
                    return raw, mime
        except Exception:
            return None, None

        return None, None

    def _mime_to_ext(self, mime):
        return {
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/webp": ".webp",
        }.get(mime or "image/png", ".png")

    def _error_message(self, response):
        try:
            data = response.json()
            msg = (
                data.get("error", {})
                .get("message")
                or data.get("error")
                or response.text[:200]
            )
            return str(msg)
        except Exception:
            return response.text[:200]
