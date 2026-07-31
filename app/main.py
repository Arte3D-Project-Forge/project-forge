import os
import sys

import customtkinter as ctk

from app.core.config_manager import ConfigManager
from app.modules.production.ui.production_window import ProductionWindow
from app.ui.project_wizard import ProjectWizard
from app.ui.project_dashboard import ProjectDashboard
from app.ui.settings_window import SettingsWindow
from app.ui.sprite_viewer import SpriteViewer


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def default_project():

    if getattr(sys, "frozen", False):
        base = os.path.join(
            os.environ.get(
                "APPDATA",
                os.path.expanduser("~")
            ),
            "ProjectForge"
        )
    else:
        base = os.path.abspath(".")

    path = os.path.join(base, "MeuJogo")

    os.makedirs(
        os.path.join(path, "sprites"),
        exist_ok=True
    )

    return {
        "name": "Meu Jogo",
        "engine": "Godot",
        "path": path
    }


class ForgeApp(ctk.CTk):

    CREATE_ITEMS = [
        ("Personagem", "Character"),
        ("Inimigo (Mob)", "Mob"),
        ("Pet / Companheiro", "Pet"),
        ("Item / Equipamento", "Item"),
        ("Mapa (Tiles)", "Tiles"),
        ("Dungeon", "Dungeon"),
        ("Efeito", "Effects")
    ]

    def __init__(self):

        super().__init__()

        self.title("Project Forge")
        self.geometry("900x620")

        self.config = ConfigManager()
        self.project = default_project()

        self.create_ui()

    # ==========================
    # UI
    # ==========================

    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="PROJECT FORGE",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=(35, 0))

        subtitle = ctk.CTkLabel(
            self,
            text="Crie personagens, mapas e assets para o seu jogo",
            font=("Arial", 15)
        )
        subtitle.pack(pady=(0, 20))

        section = ctk.CTkLabel(
            self,
            text="O QUE VOCÊ QUER CRIAR?",
            font=("Arial", 17, "bold")
        )
        section.pack(pady=(5, 5))

        self.create_category_grid()

        footer = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        footer.pack(pady=20)

        btn_gallery = ctk.CTkButton(
            footer,
            text="VER SPRITES GERADOS",
            fg_color="green",
            hover_color="darkgreen",
            height=40,
            font=("Arial", 13, "bold"),
            command=self.open_gallery
        )
        btn_gallery.pack(
            side="left",
            padx=8
        )

        btn_settings = ctk.CTkButton(
            footer,
            text="Configurações",
            height=40,
            command=self.open_settings
        )
        btn_settings.pack(
            side="left",
            padx=8
        )

        btn_exit = ctk.CTkButton(
            footer,
            text="Sair",
            height=40,
            fg_color="gray",
            hover_color="darkgray",
            command=self.destroy
        )
        btn_exit.pack(
            side="left",
            padx=8
        )

        note = ctk.CTkLabel(
            self,
            text=(
                "Geração automática: qualidade otimizada para sprites de jogo. "
                "Sem configuração necessária."
            ),
            font=("Arial", 11),
            text_color="gray"
        )
        note.pack(side="bottom", pady=10)

    def create_category_grid(self):

        grid = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        grid.pack(padx=40)

        cols = 3
        row = None

        for index, (label, category) in enumerate(
            self.CREATE_ITEMS
        ):

            if index % cols == 0:
                row = ctk.CTkFrame(
                    grid,
                    fg_color="transparent"
                )
                row.pack(pady=4)

            button = ctk.CTkButton(
                row,
                text=label,
                width=250,
                height=55,
                font=("Arial", 14, "bold"),
                command=lambda c=category:
                    self.create_asset(c)
            )
            button.pack(
                side="left",
                padx=6
            )

    # ==========================
    # AÇÕES
    # ==========================

    def create_asset(self, category):

        window = ProductionWindow(
            self,
            self.project,
            category=category
        )
        window.focus()

    def open_gallery(self):

        viewer = SpriteViewer(
            self,
            self.project
        )
        viewer.focus()

    def open_settings(self):

        window = SettingsWindow(self)
        window.focus()

    def new_project(self):

        wizard = ProjectWizard(self)
        wizard.focus()

    def open_project(self):

        dashboard = ProjectDashboard(self)
        dashboard.focus()


def main():

    print(">>> MAIN EXECUTOU <<<")

    app = ForgeApp()
    app.mainloop()
