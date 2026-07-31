import threading
import customtkinter as ctk
from tkinter import messagebox

from app.core.config_manager import ConfigManager
from app.production.production_job import ProductionJob
from app.production.pipeline.pipeline_runner import PipelineRunner
from app.ui.forge_view import (
    ACCENT,
    BG,
    CARD_BG,
    CARD_HOVER,
    MUTED,
    TEXT,
    ForgeView,
    font,
)

CATEGORIES = [
    "Character",
    "Mob",
    "Pet",
    "Item",
    "Tiles",
    "Dungeon",
    "Effects",
]

ANIMATIONS = [
    "idle",
    "walk",
    "run",
    "attack",
    "hurt",
    "death",
]

STYLE_PRESETS = [
    ("Pixel Art Retro", "pixel art, 8-bit, retro, hard pixels, limited palette"),
    ("Pixel HD", "pixel art, 16-bit, HD, crisp pixels, vibrant colors"),
    ("Anime Cel", "anime style, cel shading, clean bold outlines"),
    ("Cartoon", "cartoon style, smooth, colorful, playful"),
    ("Dark Fantasy", "dark fantasy, moody, dramatic, gothic"),
    ("Cyberpunk", "cyberpunk, neon, futuristic, high tech"),
    ("Chibi", "chibi, cute, adorable, soft colors"),
    ("Fantasy RPG", "fantasy RPG, medieval, epic, detailed"),
]

ANIMATION_PRESETS = [
    ("Idle", "idle"),
    ("Walk", "walk"),
    ("Run", "run"),
    ("Attack", "attack"),
    ("Hurt", "hurt"),
    ("Death", "death"),
]

RESOLUTIONS = ["512x512", "1024x1024"]

DEFAULT_STYLE = "pixel art, 16bit, HD RPG style, high quality"


class ProductionView(ForgeView):
    """Estúdio de produção (frame da janela única)."""

    def __init__(self, master, app=None, project=None, category=None):
        super().__init__(master, app=app, project=project)
        self.initial_category = category
        self.config = ConfigManager()
        self.build_ui()

    # ==========================
    # UI
    # ==========================

    def build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(22, 4))

        if self.has_app():
            btn_back = ctk.CTkButton(
                header,
                text="← Início",
                width=90,
                height=30,
                corner_radius=8,
                fg_color=CARD_BG,
                hover_color=CARD_HOVER,
                font=font(12, "bold"),
                command=lambda: self.navigate("home"),
            )
            btn_back.pack(side="left")

        title = ctk.CTkLabel(
            header,
            text="FORGE PRODUCTION STUDIO",
            font=font(24, "bold"),
            text_color=TEXT,
        )
        title.pack(side="left", padx=16)

        subtitle = ctk.CTkLabel(
            self,
            text="Crie sprites e assets para seu jogo com presets rápidos",
            font=font(13),
            text_color=MUTED,
        )
        subtitle.pack(pady=(0, 12))

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=30)

        # --- Configuração ---
        config_frame = ctk.CTkFrame(body, fg_color=CARD_BG, corner_radius=14)
        config_frame.pack(fill="x", pady=(0, 12))

        row1 = ctk.CTkFrame(config_frame, fg_color="transparent")
        row1.pack(pady=(14, 6), padx=18, fill="x")

        ctk.CTkLabel(row1, text="Categoria:", font=font(13), text_color=TEXT).pack(
            side="left", padx=(0, 8)
        )
        self.category_box = ctk.CTkComboBox(
            row1,
            values=CATEGORIES,
            width=150,
            state="readonly",
            font=font(13),
            button_color=ACCENT,
            button_hover_color="#6d28d9",
        )
        self.category_box.pack(side="left", padx=(0, 24))
        self.category_box.set(
            self.initial_category
            if self.initial_category in CATEGORIES
            else "Character"
        )

        ctk.CTkLabel(row1, text="Animação:", font=font(13), text_color=TEXT).pack(
            side="left", padx=(0, 8)
        )
        self.animation_box = ctk.CTkComboBox(
            row1,
            values=ANIMATIONS,
            width=120,
            state="readonly",
            font=font(13),
            button_color=ACCENT,
            button_hover_color="#6d28d9",
        )
        self.animation_box.pack(side="left", padx=(0, 24))
        self.animation_box.set("idle")

        ctk.CTkLabel(row1, text="Resolução:", font=font(13), text_color=TEXT).pack(
            side="left", padx=(0, 8)
        )
        self.size_box = ctk.CTkComboBox(
            row1,
            values=RESOLUTIONS,
            width=120,
            state="readonly",
            font=font(13),
            button_color=ACCENT,
            button_hover_color="#6d28d9",
        )
        self.size_box.pack(side="left")
        self.size_box.set(
            self.config.get("generation", "default_resolution")
            or "1024x1024"
        )

        # Presets de animação (chips)
        ctk.CTkLabel(
            config_frame,
            text="Presets de animação:",
            font=font(11, "bold"),
            text_color=MUTED,
        ).pack(padx=18, pady=(10, 4), anchor="w")

        anim_row = ctk.CTkFrame(config_frame, fg_color="transparent")
        anim_row.pack(padx=18, pady=(0, 6), fill="x")

        for label, value in ANIMATION_PRESETS:
            chip = ctk.CTkButton(
                anim_row,
                text=label,
                width=74,
                height=28,
                corner_radius=14,
                fg_color=BG,
                hover_color=CARD_HOVER,
                text_color=TEXT,
                font=font(11, "bold"),
                command=lambda v=value: self.animation_box.set(v),
            )
            chip.pack(side="left", padx=(0, 6))

        # Presets de estilo (chips)
        ctk.CTkLabel(
            config_frame,
            text="Presets de estilo:",
            font=font(11, "bold"),
            text_color=MUTED,
        ).pack(padx=18, pady=(10, 4), anchor="w")

        style_row = ctk.CTkFrame(config_frame, fg_color="transparent")
        style_row.pack(padx=18, pady=(0, 6), fill="x")

        for label, prompt in STYLE_PRESETS:
            chip = ctk.CTkButton(
                style_row,
                text=label,
                height=28,
                corner_radius=14,
                fg_color=BG,
                hover_color=CARD_HOVER,
                text_color=TEXT,
                font=font(11, "bold"),
                command=lambda p=prompt: self.apply_style(p),
            )
            chip.pack(side="left", padx=(0, 6))

        # --- Estilo / Prompt ---
        ctk.CTkLabel(
            body,
            text="Estilo:",
            font=font(13, "bold"),
            text_color=TEXT,
        ).pack(pady=(8, 4), anchor="w")

        self.style_entry = ctk.CTkEntry(
            body,
            height=36,
            corner_radius=8,
            fg_color=CARD_BG,
            border_width=0,
            text_color=TEXT,
            font=font(12),
        )
        self.style_entry.pack(fill="x")
        self.style_entry.insert(0, DEFAULT_STYLE)

        ctk.CTkLabel(
            body,
            text="Descreva o asset:",
            font=font(13, "bold"),
            text_color=TEXT,
        ).pack(pady=(12, 4), anchor="w")

        self.prompt = ctk.CTkTextbox(
            body,
            height=120,
            corner_radius=10,
            fg_color=CARD_BG,
            border_width=0,
            text_color=TEXT,
            font=font(13),
        )
        self.prompt.pack(fill="x")

        hint = ctk.CTkLabel(
            body,
            text="Ex: fire dragon com asas, espadachim com armadura dourada, slime verde gigante...",
            font=font(11),
            text_color=MUTED,
        )
        hint.pack(pady=(4, 0), anchor="w")

        # --- Ações ---
        actions = ctk.CTkFrame(body, fg_color="transparent")
        actions.pack(fill="x", pady=14)

        self.btn_criar = ctk.CTkButton(
            actions,
            text="🚀  CRIAR JOB",
            height=44,
            corner_radius=10,
            fg_color=ACCENT,
            hover_color="#6d28d9",
            text_color="white",
            font=font(14, "bold"),
            command=self.create_job,
        )
        self.btn_criar.pack(side="left", padx=(0, 10))

        self.btn_gallery = ctk.CTkButton(
            actions,
            text="🖼️  VER SPRITES GERADOS",
            height=44,
            corner_radius=10,
            fg_color=CARD_BG,
            hover_color=CARD_HOVER,
            font=font(13, "bold"),
            command=self.open_gallery,
        )
        self.btn_gallery.pack(side="left")

        # --- Status ---
        self.status = ctk.CTkLabel(
            body,
            text="Aguardando produção...",
            font=font(13, "bold"),
            text_color=MUTED,
        )
        self.status.pack(pady=(6, 0))

        self.detail_label = ctk.CTkLabel(
            body,
            text="",
            font=font(11),
            text_color=MUTED,
        )
        self.detail_label.pack(pady=2)

    def apply_style(self, prompt):
        self.style_entry.delete(0, "end")
        self.style_entry.insert(0, prompt)

    def open_gallery(self):
        if self.has_app():
            self.navigate("gallery")
        else:
            from app.ui.sprite_viewer import SpriteViewer

            viewer = SpriteViewer(self.winfo_toplevel(), self.project)
            viewer.focus()

    # ==========================
    # PRODUÇÃO
    # ==========================

    def create_job(self):
        request = self.prompt.get("1.0", "end").strip()

        if not request:
            messagebox.showwarning("Forge", "Digite o que deseja criar.")
            return

        category = self.category_box.get()
        animation = self.animation_box.get()
        resolution = self.size_box.get()
        style = self.style_entry.get().strip()

        if resolution != self.config.get("generation", "default_resolution"):
            self.config.set("generation", "default_resolution", resolution)

        enhanced_prompt = (
            f"{request}, {category.lower()} asset, "
            f"{style}, game sprite"
        )

        job = ProductionJob(
            self.project,
            enhanced_prompt,
            ["sprites"],
        )

        path = job.save()
        self.status.configure(text="Produzindo...", text_color=ACCENT)
        self.detail_label.configure(
            text=f"Categoria: {category} | Animação: {animation}"
        )
        self.btn_criar.configure(state="disabled", text="⏳ GERANDO...")

        def job_done():
            self.status.configure(text="JOB CONCLUÍDO!", text_color="green")
            self.detail_label.configure(text="")
            self.btn_criar.configure(state="normal", text="🚀  CRIAR JOB")
            self.open_gallery()

        def job_error(error_msg):
            self.status.configure(text="ERRO", text_color="red")
            self.detail_label.configure(
                text=f"{error_msg}",
                text_color="red",
            )
            self.btn_criar.configure(state="normal", text="🚀  CRIAR JOB")
            messagebox.showerror(
                "Erro",
                f"Não foi possível gerar as sprites:\n\n{error_msg}\n\n"
                "O app tentou vários geradores gratuitos automaticamente. "
                "Verifique sua conexão com a internet e tente novamente.",
            )

        def run_pipeline():
            try:
                runner = PipelineRunner(job)
                runner.run()
                self.after(0, job_done)
            except Exception as e:
                self.after(0, job_error, str(e))

        threading.Thread(target=run_pipeline, daemon=True).start()


class ProductionWindow(ctk.CTkToplevel):
    """Wrapper legado: abre o estúdio em janela própria."""

    def __init__(self, parent=None, project=None, category=None):
        super().__init__(parent)

        self.project = project or {
            "name": "Forge_Test_02",
            "engine": "Godot",
            "path": "Forge_Test_02",
        }

        self.title("Forge Production Studio")
        self.geometry("820x760")

        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))

        view = ProductionView(
            self,
            app=None,
            project=self.project,
            category=category,
        )
        view.pack(fill="both", expand=True)
