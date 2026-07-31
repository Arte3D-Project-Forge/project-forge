"""
Project Forge — Art Studio Module
Responsável pela geração de sprites e concept art via IA.
Provider padrão: Pollinations.ai (gratuito, sem API key)
"""

import os
import json
from datetime import datetime


class ArtStudioModule:
    """
    Módulo de geração de arte para o Project Forge.
    Segue a interface ForgeModule (name, version, lifecycle, services).
    """

    name = "art_studio"
    version = "1.0.0"

    def __init__(self, project_path: str = None):
        self.project_path = project_path
        self.provider = "pollinations"
        self.history: list[dict] = []
        self._history_file = None

        if project_path:
            self._setup_paths(project_path)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def initialize(self, project_path: str) -> None:
        """Inicializa o módulo com o caminho do projeto."""
        self.project_path = project_path
        self._setup_paths(project_path)
        self._load_history()

    def _setup_paths(self, project_path: str) -> None:
        self.assets_dir = os.path.join(project_path, "assets", "sprites")
        self.history_dir = os.path.join(project_path, "data", "art_studio")
        self._history_file = os.path.join(self.history_dir, "generation_history.json")

        os.makedirs(self.assets_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Services
    # ------------------------------------------------------------------

    def generate_sprite(
        self,
        prompt: str,
        width: int = 512,
        height: int = 512,
        style: str = "pixel art",
        save_name: str = None,
    ) -> dict:
        """
        Gera um sprite via Pollinations.ai e salva no projeto.

        Retorna:
            {
                "success": bool,
                "file_path": str | None,
                "url": str,
                "prompt": str,
                "timestamp": str,
                "error": str | None
            }
        """
        from app.services.pollinations_service import PollinationsService

        service = PollinationsService()
        full_prompt = f"{style}, {prompt}, transparent background, game asset, top-down RPG"

        result = service.generate_image(
            prompt=full_prompt,
            width=width,
            height=height,
        )

        if result["success"] and self.project_path:
            filename = save_name or self._make_filename(prompt)
            file_path = os.path.join(self.assets_dir, filename)
            save_result = service.save_image(result["image_data"], file_path)
            result["file_path"] = file_path if save_result else None
        else:
            result["file_path"] = None

        result["prompt"] = prompt
        result["style"] = style
        result["timestamp"] = datetime.now().isoformat()

        self._record_history(result)
        return result

    def get_history(self) -> list[dict]:
        """Retorna o histórico de gerações."""
        return self.history

    def get_providers(self) -> list[dict]:
        """Lista provedores disponíveis e seus status."""
        return [
            {
                "id": "pollinations",
                "name": "Pollinations.ai",
                "status": "free",
                "requires_key": False,
                "description": "Gratuito, sem cadastro. Ótimo para protótipos.",
            },
            {
                "id": "huggingface",
                "name": "Hugging Face Inference",
                "status": "free_with_key",
                "requires_key": True,
                "description": "Gratuito com conta. Modelos especializados em pixel art.",
            },
        ]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _make_filename(self, prompt: str) -> str:
        slug = prompt[:30].lower().replace(" ", "_")
        slug = "".join(c for c in slug if c.isalnum() or c == "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"sprite_{slug}_{timestamp}.png"

    def _record_history(self, result: dict) -> None:
        self.history.append(result)
        if self._history_file:
            try:
                with open(self._history_file, "w", encoding="utf-8") as f:
                    json.dump(self.history, f, ensure_ascii=False, indent=2)
            except Exception:
                pass

    def _load_history(self) -> None:
        if self._history_file and os.path.exists(self._history_file):
            try:
                with open(self._history_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []
