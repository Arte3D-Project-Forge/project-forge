import os

import customtkinter as ctk
from PIL import Image

from app.ui.forge_view import (
    ACCENT,
    CARD_BG,
    CARD_HOVER,
    MUTED,
    TEXT,
    ForgeView,
    font,
)


class GalleryView(ForgeView):
    """Galeria de sprites (frame da janela única)."""

    def __init__(self, master, app=None, project=None):
        super().__init__(master, app=app, project=project)
        self.build_ui()
        self.load_sprites()

    def build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(22, 10))

        if self.has_app():
            btn_back = ctk.CTkButton(
                header,
                text="← Voltar",
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
            text="GALERIA DE SPRITES",
            font=font(24, "bold"),
            text_color=TEXT,
        )
        title.pack(side="left", padx=16)

        refresh = ctk.CTkButton(
            header,
            text="🔄 Atualizar",
            width=100,
            height=30,
            corner_radius=8,
            fg_color=ACCENT,
            hover_color="#6d28d9",
            font=font(12, "bold"),
            command=self.load_sprites,
        )
        refresh.pack(side="right")

        self.canvas_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=10,
        )
        self.canvas_frame.pack(
            padx=30,
            pady=(0, 12),
            fill="both",
            expand=True,
        )

        self.status = ctk.CTkLabel(
            self,
            text="",
            font=font(12),
            text_color=MUTED,
        )
        self.status.pack(pady=(0, 10))

    def load_sprites(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        sprite_path = os.path.join(self.project["path"], "sprites")

        debug_lines = [f"Procurando em: {sprite_path}"]

        if not os.path.exists(sprite_path):
            debug_lines.append("PASTA NAO EXISTE")
            self.status.configure(text="\n".join(debug_lines))
            return

        all_files = []
        for root, dirs, files in os.walk(sprite_path):
            for f in files:
                fp = os.path.join(root, f)
                all_files.append(fp)

        debug_lines.append(f"Total arquivos: {len(all_files)}")

        images = []
        for fp in all_files:
            if fp.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                images.append(fp)
            else:
                debug_lines.append(f"  Ignorado: {os.path.basename(fp)}")

        if not images:
            if all_files:
                debug_lines.append("Nenhum arquivo de imagem valido")
                for f in all_files[:5]:
                    debug_lines.append(f"  {os.path.relpath(f, sprite_path)[:60]}")
            else:
                debug_lines.append("Pasta vazia")
            self.status.configure(text="\n".join(debug_lines))
            return

        self.status.configure(text=f"{len(images)} sprites encontrados")

        cols = 4
        row_frame = None

        for i, img_path in enumerate(images):
            if i % cols == 0:
                row_frame = ctk.CTkFrame(
                    self.canvas_frame,
                    fg_color="transparent",
                )
                row_frame.pack(fill="x", pady=5)

            try:
                pil_image = Image.open(img_path)
                pil_image.thumbnail((180, 180), Image.LANCZOS)

                ctk_image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(pil_image.width, pil_image.height),
                )

                card = ctk.CTkFrame(
                    row_frame,
                    width=200,
                    fg_color=CARD_BG,
                    corner_radius=12,
                )
                card.pack(side="left", padx=5, fill="both", expand=True)
                card.pack_propagate(False)

                label = ctk.CTkLabel(
                    card,
                    text="",
                    image=ctk_image,
                )
                label.pack(pady=8)

                name = ctk.CTkLabel(
                    card,
                    text=os.path.basename(img_path),
                    font=font(10),
                    text_color=MUTED,
                )
                name.pack(pady=(0, 8))

            except Exception:
                pass


class SpriteViewer(ctk.CTkToplevel):
    """Wrapper legado: abre a galeria em janela própria."""

    def __init__(self, parent, project):
        super().__init__(parent)

        self.project = project

        self.after(50, lambda: (self.lift(), self.focus_force()))

        self.title(f"Sprites - {project['name']}")

        self.geometry("900x700")

        view = GalleryView(self, app=None, project=self.project)
        view.pack(fill="both", expand=True)
