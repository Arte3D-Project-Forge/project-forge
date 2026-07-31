import customtkinter as ctk

ACCENT = "#7c3aed"
ACCENT_HOVER = "#6d28d9"
BG = "#0f1117"
SIDEBAR_BG = "#151922"
CARD_BG = "#1e2531"
CARD_HOVER = "#2a3443"
TEXT = "#e8ecf2"
MUTED = "#8b93a5"
GREEN = "#22c55e"
GREEN_HOVER = "#16a34a"
RED = "#ef4444"
GRAY = "#6b7280"

FONT_FAMILY = "Segoe UI"


def font(size=12, weight="normal"):
    return (FONT_FAMILY, size, weight)


class ForgeView(ctk.CTkFrame):
    """Tela base da janela única.

    Cada tela (Início, Estúdio, Galeria, Configurações) é um frame
    que recebe a referência do app para navegar entre telas.
    """

    def __init__(self, master, app=None, project=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.app = app
        self.project = project or {
            "name": "Meu Jogo",
            "engine": "Godot",
            "path": "MeuJogo"
        }

    def navigate(self, view, **kwargs):
        if self.app is not None:
            self.app.show_view(view, **kwargs)

    def has_app(self):
        return self.app is not None
