import os
import sys

import customtkinter as ctk

from app.core.config_manager import ConfigManager
from app.modules.production.ui.production_window import ProductionView
from app.ui.forge_view import (
    ACCENT,
    ACCENT_HOVER,
    BG,
    GRAY,
    GREEN,
    MUTED,
    SIDEBAR_BG,
    TEXT,
    font,
)
from app.ui.home_view import HomeView
from app.ui.settings_window import SettingsView
from app.ui.sprite_viewer import GalleryView


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
    """Janela única: sidebar de navegação + telas (sem abrir guias novas)."""

    VIEWS = {
        "home": HomeView,
        "studio": ProductionView,
        "gallery": GalleryView,
        "settings": SettingsView,
    }

    NAV_ITEMS = [
        ("home", "🏠  Início"),
        ("studio", "⚡  Criar Asset"),
        ("gallery", "🖼️  Galeria"),
        ("settings", "⚙️  Configurações"),
    ]

    def __init__(self):
        super().__init__()

        self.title("Project Forge")
        self.geometry("1080x740")
        self.minsize(960, 640)

        self.config = ConfigManager()
        self.project = default_project()

        self.build_ui()

        self._start_sync_poller()
        self._start_status_poller()

    # ==========================
    # UI
    # ==========================

    def build_ui(self):
        self.configure(fg_color=BG)

        self.sidebar = ctk.CTkFrame(
            self,
            width=210,
            fg_color=SIDEBAR_BG,
            corner_radius=0,
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

        self._build_sidebar()
        self.show_view("home")

    def _build_sidebar(self):
        logo = ctk.CTkLabel(
            self.sidebar,
            text="PROJECT\nFORGE",
            font=font(20, "bold"),
            text_color=ACCENT,
            justify="center",
        )
        logo.pack(pady=(28, 4))

        tagline = ctk.CTkLabel(
            self.sidebar,
            text="AI Game Dev OS",
            font=font(11),
            text_color=MUTED,
        )
        tagline.pack(pady=(0, 24))

        self.nav_buttons = {}

        for view, label in self.NAV_ITEMS:
            button = ctk.CTkButton(
                self.sidebar,
                text=label,
                height=42,
                corner_radius=10,
                fg_color="transparent",
                hover_color=ACCENT_HOVER,
                text_color=TEXT,
                anchor="w",
                font=font(13, "bold"),
                command=lambda v=view: self.show_view(v),
            )
            button.pack(fill="x", padx=14, pady=4)
            self.nav_buttons[view] = button

        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        self.status_dot = ctk.CTkLabel(
            self.sidebar,
            text="●",
            font=font(14),
            text_color=GRAY,
        )
        self.status_dot.pack(pady=(0, 0))

        self.status_label = ctk.CTkLabel(
            self.sidebar,
            text="ComfyUI: offline",
            font=font(11),
            text_color=MUTED,
        )
        self.status_label.pack(pady=(0, 16))

    def show_view(self, view, **kwargs):
        for widget in self.content.winfo_children():
            widget.destroy()

        view_class = self.VIEWS[view]
        instance = view_class(
            self.content,
            app=self,
            project=self.project,
            **kwargs,
        )
        instance.pack(fill="both", expand=True)

        for name, button in self.nav_buttons.items():
            if name == view:
                button.configure(fg_color=ACCENT)
            else:
                button.configure(fg_color="transparent")

    # ==========================
    # STATUS COMfyUI
    # ==========================

    def _start_sync_poller(self):
        from app.services.comfyui_sync import (
            ComfyUISyncPoller
        )

        try:
            self.sync_poller = ComfyUISyncPoller(
                self.config
            )
            self.sync_poller.start()
        except Exception:
            self.sync_poller = None

    def _start_status_poller(self):
        import threading
        import time

        from app.services.comfyui_sync import ComfyUISync

        def poll():
            while True:
                time.sleep(10)
                url = (
                    self.config.config.get("comfyui", {})
                    .get("server_url", "")
                    .strip()
                    .rstrip("/")
                )
                online = bool(url) and ComfyUISync.url_alive(url)
                self.after(0, lambda ok=online: self._update_status(ok))

        threading.Thread(target=poll, daemon=True).start()

    def _update_status(self, online):
        self.status_dot.configure(
            text_color=GREEN if online else GRAY
        )
        self.status_label.configure(
            text="ComfyUI: conectado" if online else "ComfyUI: offline",
            text_color=GREEN if online else MUTED,
        )


def main():

    print(">>> MAIN EXECUTOU <<<")

    app = ForgeApp()
    app.mainloop()
