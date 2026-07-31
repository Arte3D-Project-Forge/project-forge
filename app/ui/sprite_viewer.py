import customtkinter as ctk
import os

from PIL import Image, ImageTk


class SpriteViewer(ctk.CTkToplevel):

    def __init__(self, parent, project):

        super().__init__(parent)

        self.project = project

        self.after(50, lambda: (self.lift(), self.focus_force()))

        self.title(
            f"Sprites - {project['name']}"
        )

        self.geometry("900x700")

        self.create_ui()


    def create_ui(self):

        header = ctk.CTkLabel(
            self,
            text="GALERIA DE SPRITES",
            font=("Arial", 28, "bold")
        )

        header.pack(pady=20)

        self.canvas_frame = ctk.CTkScrollableFrame(
            self,
            width=800,
            height=500
        )

        self.canvas_frame.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        refresh = ctk.CTkButton(
            self,
            text="ATUALIZAR",
            command=self.load_sprites
        )

        refresh.pack(pady=10)

        self.status = ctk.CTkLabel(
            self,
            text=""
        )

        self.status.pack(pady=5)

        self.load_sprites()


    def load_sprites(self):

        for widget in (
            self.canvas_frame.winfo_children()
        ):
            widget.destroy()

        sprite_path = os.path.join(
            self.project["path"],
            "sprites"
        )

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

        self.status.configure(
            text=f"{len(images)} sprites encontrados"
        )

        cols = 4
        row_frame = None

        for i, img_path in enumerate(images):

            if i % cols == 0:

                row_frame = ctk.CTkFrame(
                    self.canvas_frame
                )

                row_frame.pack(
                    fill="x",
                    pady=5
                )

            try:

                pil_image = Image.open(
                    img_path
                )

                pil_image.thumbnail(
                    (180, 180),
                    Image.LANCZOS
                )

                ctk_image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(
                        pil_image.width,
                        pil_image.height
                    )
                )

                card = ctk.CTkFrame(
                    row_frame,
                    width=200
                )

                card.pack(
                    side="left",
                    padx=5,
                    fill="both",
                    expand=True
                )

                label = ctk.CTkLabel(
                    card,
                    text="",
                    image=ctk_image
                )

                label.pack(pady=5)

                name = ctk.CTkLabel(
                    card,
                    text=os.path.basename(
                        img_path
                    ),
                    font=("Arial", 10)
                )

                name.pack()

            except Exception:

                pass
