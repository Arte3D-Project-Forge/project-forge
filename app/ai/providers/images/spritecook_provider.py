import os
import httpx

from datetime import datetime

from app.ai.providers.images.image_provider import ImageProvider


class SpriteCookProvider(ImageProvider):
    """
    SpriteCook - gerador de sprites pixel art nivel estudio.

    API REST com pixel art real em grid, fundo transparente nativo,
    paleta de cores e consistencia via imagem de referencia.

    Precos:
    - 40 creditos gratis por mes (sem cartao)
    - ~8 creditos por sprite
    - Planos: $8/mo (800 creditos), $30/mo (3000), $70/mo (7000)

    Docs: https://spritecook.ai/api-docs
    """

    API_BASE = "https://api.spritecook.ai/v1/api"
    DEFAULT_MODEL = "gemini-3.1-flash-image"

    def __init__(self):
        from app.core.config_manager import ConfigManager

        config = ConfigManager()
        cfg = config.config.get("spritecook", {})
        generation = config.config.get("generation", {})
        resolution = generation.get(
            "default_resolution", "512x512"
        ).lower().split("x")

        self.api_key = (
            cfg.get("api_key", "")
            or os.environ.get("SPRITECOOK_API_KEY", "")
        )
        self.model = cfg.get("model", self.DEFAULT_MODEL)
        self.resolution = cfg.get("resolution", "1K")
        self.quality = cfg.get("quality", "medium")
        self.pixel = cfg.get("pixel", True)
        self.pixel_perfect = cfg.get("pixel_perfect", True)
        self.bg_mode = cfg.get("bg_mode", "transparent")
        self.theme = cfg.get("theme", "")
        self.colors = cfg.get("colors", [])
        self.variations = int(cfg.get("variations", 4) or 4)
        self.width = int(resolution[0])
        self.height = int(resolution[1])
        self.timeout = 600
        self.client = httpx.Client(
            timeout=httpx.Timeout(self.timeout),
            follow_redirects=True,
            verify=False,
        )

    def is_configured(self):
        return bool(self.api_key)

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate(self, prompt, filename, output_path):
        if not self.is_configured():
            return {
                "status": "error",
                "provider": "spritecook",
                "error": (
                    "SpriteCook sem API key. Configure a chave em "
                    "Configuracoes > Gerador (spritecook) ou "
                    "SPRITECOOK_API_KEY no ambiente."
                ),
            }

        os.makedirs(output_path, exist_ok=True)
        last_error = "erro desconhecido"

        try:
            payload = {
                "prompt": prompt,
                "width": self.width,
                "height": self.height,
                "variations": self.variations,
                "pixel": self.pixel,
                "pixel_perfect": self.pixel_perfect,
                "bg_mode": self.bg_mode,
                "model": self.model,
                "resolution": self.resolution,
                "quality": self.quality,
            }
            if self.theme:
                payload["theme"] = self.theme
            if self.colors:
                payload["colors"] = self.colors

            response = self.client.post(
                f"{self.API_BASE}/generate-sync",
                json=payload,
                headers=self._headers(),
            )

            if response.status_code not in (200, 202):
                return {
                    "status": "error",
                    "provider": "spritecook",
                    "error": (
                        f"SpriteCook HTTP {response.status_code}: "
                        f"{self._error_message(response)}"
                    ),
                }

            data = response.json()
            assets = self._extract_assets(data)

            if not assets:
                return {
                    "status": "error",
                    "provider": "spritecook",
                    "error": "SpriteCook retornou sem assets.",
                }

            saved = []
            for i, asset in enumerate(assets):
                file_path = self._save_asset(asset, filename, output_path, i)
                if file_path:
                    saved.append(file_path)

            if not saved:
                return {
                    "status": "error",
                    "provider": "spritecook",
                    "error": "Nenhum asset pôde ser salvo.",
                }

            return {
                "status": "generated",
                "provider": "spritecook",
                "model": self.model,
                "files": saved,
                "created_at": datetime.now().isoformat(),
            }

        except httpx.ConnectError as e:
            last_error = f"Sem conexao com o servidor: {e}"
        except Exception as e:
            last_error = f"{type(e).__name__}: {e}"

        return {
            "status": "error",
            "provider": "spritecook",
            "error": last_error,
        }

    def _error_message(self, response):
        try:
            data = response.json()
            return data.get("error") or data.get("message") or response.text[:200]
        except Exception:
            return response.text[:200]

    def _extract_assets(self, data):
        """Extrai a lista de assets do retorno do SpriteCook.

        Formatos possiveis (robusto a mudancas da API):
        - {"output": [{"url": "..."}]}
        - {"assets": [{"url": "..."}]}
        - {"output": [{"image_url": "..."}]}
        - {"output": [{"file": {"url": "..."}}]}
        - {"data": {"output": [...]}}
        """
        if not isinstance(data, dict):
            return []

        candidates = []
        for key in ("data", "result"):
            if isinstance(data.get(key), dict):
                candidates.append(data[key])

        candidates.append(data)

        for block in candidates:
            for key in ("output", "assets", "results"):
                items = block.get(key)
                if isinstance(items, list) and items:
                    return items

        return []

    def _save_asset(self, asset, filename, output_path, index):
        url = None
        if isinstance(asset, dict):
            for key in ("url", "image_url", "download_url"):
                if asset.get(key):
                    url = asset[key]
                    break
            if not url:
                file_info = asset.get("file")
                if isinstance(file_info, dict):
                    url = file_info.get("url")

        if not url:
            return None

        if url.startswith("data:"):
            import base64

            raw = base64.b64decode(url.split(",", 1)[1])
            ext = ".png"
        else:
            resp = self.client.get(url)
            if resp.status_code != 200 or not resp.content:
                return None
            raw = resp.content
            ext = ".png"
            ct = resp.headers.get("Content-Type", "")
            if "png" in ct:
                ext = ".png"
            elif "jpeg" in ct or "jpg" in ct:
                ext = ".jpg"
            elif "webp" in ct:
                ext = ".webp"

        name = filename if self.variations <= 1 else f"{filename}_{index + 1}"
        file_path = os.path.join(output_path, name + ext)
        with open(file_path, "wb") as f:
            f.write(raw)

        return file_path
