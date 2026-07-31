"""
Project Forge — Pollinations.ai Service
Provider de geração de imagens gratuito e sem API key.
Documentação: https://pollinations.ai
"""

import urllib.request
import urllib.parse
import urllib.error
import os


class PollinationsService:
    """
    Serviço de geração de imagens via Pollinations.ai.
    Completamente gratuito — sem cadastro, sem API key.
    """

    BASE_URL = "https://image.pollinations.ai/prompt"

    def __init__(self):
        self.model = "flux"          # modelo padrão (melhor qualidade free)
        self.timeout = 60            # segundos

    def generate_image(
        self,
        prompt: str,
        width: int = 512,
        height: int = 512,
        seed: int = None,
    ) -> dict:
        """
        Gera uma imagem a partir de um prompt.

        Parâmetros:
            prompt  — descrição da imagem em inglês (resultados melhores)
            width   — largura em pixels (padrão 512)
            height  — altura em pixels (padrão 512)
            seed    — seed para reprodutibilidade (opcional)

        Retorna:
            {
                "success": bool,
                "image_data": bytes | None,
                "url": str,
                "error": str | None
            }
        """
        url = self._build_url(prompt, width, height, seed)

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "ProjectForge/1.0"},
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                image_data = response.read()

            return {
                "success": True,
                "image_data": image_data,
                "url": url,
                "error": None,
            }

        except urllib.error.URLError as e:
            return {
                "success": False,
                "image_data": None,
                "url": url,
                "error": f"Erro de rede: {e.reason}",
            }
        except Exception as e:
            return {
                "success": False,
                "image_data": None,
                "url": url,
                "error": str(e),
            }

    def save_image(self, image_data: bytes, file_path: str) -> bool:
        """
        Salva os bytes da imagem em disco.

        Retorna True se salvou com sucesso.
        """
        if not image_data:
            return False

        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(image_data)
            return True
        except Exception:
            return False

    def _build_url(self, prompt: str, width: int, height: int, seed: int) -> str:
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"{self.BASE_URL}/{encoded_prompt}"

        params = {
            "width": width,
            "height": height,
            "model": self.model,
            "nologo": "true",
        }
        if seed is not None:
            params["seed"] = seed

        query = urllib.parse.urlencode(params)
        return f"{url}?{query}"
