import threading
import customtkinter as ctk
from tkinter import messagebox

from app.core.config_manager import ConfigManager
from app.production.production_job import ProductionJob
from app.production.pipeline.pipeline_runner import PipelineRunner
from app.ui.sprite_viewer import SpriteViewer


class ProductionWindow(ctk.CTkToplevel):

    def __init__(self, parent=None, project=None, category=None):
        super().__init__(parent)

        self.project = project or {
            "name": "Forge_Test_02",
            "engine": "Godot",
            "path": "Forge_Test_02"
        }

        self.initial_category = category

        self.title("Forge Production Studio")
        self.geometry("800x700")

        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))

        self.categories = [
            "Character",
            "Mob",
            "Pet",
            "Item",
            "Tiles",
            "Dungeon",
            "Effects"
        ]

        self.animations = [
            "idle",
            "walk",
            "attack",
            "hurt",
            "death"
        ]

        self.config = ConfigManager()

        self.build_ui()

    def build_ui(self):
        title = ctk.CTkLabel(
            self,
            text="FORGE PRODUCTION STUDIO",
            font=("Arial", 26, "bold")
        )
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Crie sprites e assets para seu jogo"
        )
        subtitle.pack()

        # --- Config frame ---
        config_frame = ctk.CTkFrame(self)
        config_frame.pack(pady=15, padx=30, fill="x")

        row1 = ctk.CTkFrame(config_frame, fg_color="transparent")
        row1.pack(pady=(10, 5), padx=15, fill="x")

        ctk.CTkLabel(row1, text="Categoria:").pack(
            side="left", padx=(0, 10)
        )
        self.category_box = ctk.CTkComboBox(
            row1,
            values=self.categories,
            width=180,
            state="readonly"
        )
        self.category_box.pack(side="left", padx=5)
        self.category_box.set(
            self.initial_category
            if self.initial_category in self.categories
            else "Character"
        )

        ctk.CTkLabel(row1, text="Animação:").pack(
            side="left", padx=(25, 10)
        )
        self.animation_box = ctk.CTkComboBox(
            row1,
            values=self.animations,
            width=140,
            state="readonly"
        )
        self.animation_box.pack(side="left", padx=5)
        self.animation_box.set("idle")

        ctk.CTkLabel(row1, text="Resolução:").pack(
            side="left", padx=(25, 10)
        )
        self.size_box = ctk.CTkComboBox(
            row1,
            values=["512x512", "1024x1024"],
            width=120,
            state="readonly"
        )
        self.size_box.pack(side="left", padx=5)
        self.size_box.set("1024x1024")

        # Estilo
        row2 = ctk.CTkFrame(config_frame, fg_color="transparent")
        row2.pack(pady=(5, 10), padx=15, fill="x")

        ctk.CTkLabel(row2, text="Estilo:").pack(
            side="left", padx=(0, 10)
        )
        self.style_entry = ctk.CTkEntry(
            row2,
            width=500,
            placeholder_text="Ex: pixel art, 16bit, RPG style (o mesmo estilo será usado em todos os assets)"
        )
        self.style_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.style_entry.insert(0, "pixel art, 16bit, HD RPG style, high quality")

        # --- Prompt ---
        prompt_label = ctk.CTkLabel(
            self,
            text="Descreva o asset:",
            font=("Arial", 14, "bold")
        )
        prompt_label.pack(pady=(10, 0))

        self.prompt = ctk.CTkTextbox(
            self,
            width=700,
            height=120
        )
        self.prompt.pack(pady=10, padx=30)

        hint = ctk.CTkLabel(
            self,
            text="Ex: fire dragon com asas, espadachim com armadura dourada, slime verde gigante...",
            text_color="gray"
        )
        hint.pack()

        # --- Buttons ---
        self.btn_criar = ctk.CTkButton(
            self,
            text="CRIAR JOB",
            command=self.create_job,
            height=40,
            font=("Arial", 14, "bold")
        )
        self.btn_criar.pack(pady=15)

        self.btn_gallery = ctk.CTkButton(
            self,
            text="VER SPRITES GERADOS",
            command=self.open_gallery,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.btn_gallery.pack(pady=5)

        # --- Status ---
        self.status = ctk.CTkLabel(
            self,
            text="Aguardando produção...",
            font=("Arial", 13)
        )
        self.status.pack(pady=10)

        self.detail_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 11),
            text_color="gray"
        )
        self.detail_label.pack(pady=2)

    def open_gallery(self):
        viewer = SpriteViewer(self, self.project)
        viewer.focus()

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
            ["sprites"]
        )

        path = job.save()
        self.status.configure(text="Produzindo...")
        self.detail_label.configure(
            text=f"Categoria: {category} | Animação: {animation}"
        )
        self.btn_criar.configure(state="disabled", text="GERANDO...")

        def job_done():
            self.status.configure(text="JOB CONCLUÍDO!")
            self.detail_label.configure(text="")
            self.btn_criar.configure(state="normal", text="CRIAR JOB")
            self.open_gallery()

        def job_error(error_msg):
            self.status.configure(text="ERRO")
            self.detail_label.configure(
                text=f"{error_msg}",
                text_color="red"
            )
            self.btn_criar.configure(state="normal", text="CRIAR JOB")
            messagebox.showerror(
                "Erro",
                f"Não foi possível gerar as sprites:\n\n{error_msg}\n\n"
                "O app tentou vários geradores gratuitos automaticamente. "
                "Verifique sua conexão com a internet e tente novamente."
            )

        def run_pipeline():
            try:
                runner = PipelineRunner(job)
                runner.run()
                self.after(0, job_done)
            except Exception as e:
                self.after(0, job_error, str(e))

        threading.Thread(target=run_pipeline, daemon=True).start()
