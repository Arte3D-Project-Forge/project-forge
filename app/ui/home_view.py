import customtkinter as ctk

from app.ui.forge_view import (
    ACCENT,
    CARD_BG,
    CARD_HOVER,
    MUTED,
    TEXT,
    ForgeView,
    font,
)

CATEGORIES = [
    ("Personagem", "Character", "🦸"),
    ("Inimigo (Mob)", "Mob", "👹"),
    ("Pet / Companheiro", "Pet", "🐾"),
    ("Item / Equipamento", "Item", "⚔️"),
    ("Mapa (Tiles)", "Tiles", "🗺️"),
    ("Dungeon", "Dungeon", "🏰"),
    ("Efeito", "Effects", "✨"),
]


class HomeView(ForgeView):

    def __init__(self, master, app=None, project=None):
        super().__init__(master, app=app, project=project)
        self.build_ui()

    def build_ui(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=40, pady=(30, 20))

        badge = ctk.CTkLabel(
            container,
            text="⚡ AI GAME DEVELOPMENT OS",
            font=font(12, "bold"),
            text_color=ACCENT,
        )
        badge.pack(anchor="w")

        title = ctk.CTkLabel(
            container,
            text="PROJECT FORGE",
            font=font(34, "bold"),
            text_color=TEXT,
        )
        title.pack(anchor="w", pady=(2, 0))

        subtitle = ctk.CTkLabel(
            container,
            text="Crie personagens, mapas e assets de jogo em segundos",
            font=font(15),
            text_color=MUTED,
        )
        subtitle.pack(anchor="w", pady=(2, 24))

        section = ctk.CTkLabel(
            container,
            text="O QUE VOCÊ QUER CRIAR?",
            font=font(16, "bold"),
            text_color=TEXT,
        )
        section.pack(anchor="w", pady=(0, 12))

        grid = ctk.CTkFrame(container, fg_color="transparent")
        grid.pack(fill="both", expand=True)

        cols = 3
        row = None

        for index, (label, category, emoji) in enumerate(CATEGORIES):
            if index % cols == 0:
                row = ctk.CTkFrame(grid, fg_color="transparent")
                row.pack(fill="x", pady=6)

            button = ctk.CTkButton(
                row,
                text=f"{emoji}  {label}",
                width=260,
                height=78,
                corner_radius=14,
                fg_color=CARD_BG,
                hover_color=CARD_HOVER,
                text_color=TEXT,
                font=font(15, "bold"),
                command=lambda c=category: self.navigate("studio", category=c),
            )
            button.pack(side="left", padx=6, expand=True, fill="x")

        footer = ctk.CTkFrame(container, fg_color="transparent")
        footer.pack(fill="x", pady=(18, 0))

        btn_gallery = ctk.CTkButton(
            footer,
            text="🖼️  Ver sprites gerados",
            height=42,
            corner_radius=10,
            fg_color=ACCENT,
            hover_color="#6d28d9",
            font=font(13, "bold"),
            command=lambda: self.navigate("gallery"),
        )
        btn_gallery.pack(side="left", padx=(0, 8))

        btn_settings = ctk.CTkButton(
            footer,
            text="⚙️  Configurações",
            height=42,
            corner_radius=10,
            fg_color=CARD_BG,
            hover_color=CARD_HOVER,
            font=font(13, "bold"),
            command=lambda: self.navigate("settings"),
        )
        btn_settings.pack(side="left", padx=8)

        note = ctk.CTkLabel(
            container,
            text="Geração automática: qualidade otimizada para sprites de jogo.",
            font=font(11),
            text_color=MUTED,
        )
        note.pack(anchor="w", pady=(18, 0))
