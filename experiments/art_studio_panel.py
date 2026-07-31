"""
Project Forge — Art Studio Panel (CustomTkinter)
Interface para geração de sprites via IA.
"""

import threading
import io
import customtkinter as ctk
from PIL import Image, ImageTk


class ArtStudioPanel(ctk.CTkFrame):
    """
    Painel principal do Art Studio.
    Integra com ArtStudioModule para gerar sprites pixel art.
    """

    # Presets de estilo para o menu suspenso
    STYLE_PRESETS = [
        "pixel art 16x16",
        "pixel art 32x32",
        "pixel art 64x64",
        "pixel art top-down RPG",
        "pixel art character sprite sheet",
        "pixel art tileset",
        "pixel art weapon icon",
        "pixel art environment",
        "concept art RPG",
        "concept art fantasy",
    ]

    # Tamanhos disponíveis
    SIZE_OPTIONS = ["256x256", "512x512", "512x256", "256x512", "768x512"]

    def __init__(self, parent, art_module=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.art_module = art_module
        self._current_image = None       # PIL Image atual
        self._tk_image = None            # referência para evitar GC
        self._is_generating = False

        self._build_ui()

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Painel esquerdo — controles
        self._left = ctk.CTkFrame(self, width=300)
        self._left.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        self._left.grid_propagate(False)
        self._build_controls(self._left)

        # Painel direito — visualização
        self._right = ctk.CTkFrame(self)
        self._right.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        self._build_preview(self._right)

    def _build_controls(self, parent):
        parent.grid_columnconfigure(0, weight=1)

        # Título
        ctk.CTkLabel(
            parent,
            text="🎨 Art Studio",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

        ctk.CTkLabel(
            parent,
            text="Powered by Pollinations.ai (Gratuito)",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        ).grid(row=1, column=0, padx=15, pady=(0, 15), sticky="w")

        # Separador visual
        ctk.CTkFrame(parent, height=1, fg_color="gray40").grid(
            row=2, column=0, sticky="ew", padx=10, pady=5
        )

        # Prompt
        ctk.CTkLabel(
            parent,
            text="Descrição do Sprite (em inglês):",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=3, column=0, padx=15, pady=(10, 3), sticky="w")

        self._prompt_box = ctk.CTkTextbox(parent, height=100, wrap="word")
        self._prompt_box.grid(row=4, column=0, padx=15, pady=(0, 8), sticky="ew")
        self._prompt_box.insert("end", "blacksmith character, fantasy RPG, facing front")

        # Dica de prompt
        ctk.CTkLabel(
            parent,
            text="💡 Dica: escreva em inglês para melhores resultados.",
            font=ctk.CTkFont(size=10),
            text_color="gray",
            wraplength=250,
        ).grid(row=5, column=0, padx=15, pady=(0, 10), sticky="w")

        # Estilo
        ctk.CTkLabel(
            parent,
            text="Estilo:",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=6, column=0, padx=15, pady=(0, 3), sticky="w")

        self._style_var = ctk.StringVar(value=self.STYLE_PRESETS[3])
        self._style_menu = ctk.CTkOptionMenu(
            parent,
            values=self.STYLE_PRESETS,
            variable=self._style_var,
            width=260,
        )
        self._style_menu.grid(row=7, column=0, padx=15, pady=(0, 10), sticky="ew")

        # Tamanho
        ctk.CTkLabel(
            parent,
            text="Tamanho (pixels):",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=8, column=0, padx=15, pady=(0, 3), sticky="w")

        self._size_var = ctk.StringVar(value="512x512")
        self._size_menu = ctk.CTkOptionMenu(
            parent,
            values=self.SIZE_OPTIONS,
            variable=self._size_var,
            width=260,
        )
        self._size_menu.grid(row=9, column=0, padx=15, pady=(0, 15), sticky="ew")

        # Botão Gerar
        self._btn_generate = ctk.CTkButton(
            parent,
            text="✨ Gerar Sprite",
            command=self._on_generate,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#5c5fef",
            hover_color="#4547c7",
        )
        self._btn_generate.grid(row=10, column=0, padx=15, pady=(0, 8), sticky="ew")

        # Botão Salvar no Projeto
        self._btn_save = ctk.CTkButton(
            parent,
            text="💾 Salvar no Projeto",
            command=self._on_save,
            height=38,
            state="disabled",
            font=ctk.CTkFont(size=13),
            fg_color="#2a7a3b",
            hover_color="#1d5c2b",
        )
        self._btn_save.grid(row=11, column=0, padx=15, pady=(0, 8), sticky="ew")

        # Status
        self._status_label = ctk.CTkLabel(
            parent,
            text="Pronto.",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            wraplength=260,
        )
        self._status_label.grid(row=12, column=0, padx=15, pady=(5, 15), sticky="w")

    def _build_preview(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            parent,
            text="Pré-visualização",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

        # Área da imagem
        self._image_frame = ctk.CTkFrame(parent, fg_color="#1a1a2e")
        self._image_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self._image_frame.grid_columnconfigure(0, weight=1)
        self._image_frame.grid_rowconfigure(0, weight=1)

        self._image_label = ctk.CTkLabel(
            self._image_frame,
            text="Nenhuma imagem gerada ainda.\n\nDigite um prompt e clique em\n✨ Gerar Sprite",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        )
        self._image_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Progress bar
        self._progress = ctk.CTkProgressBar(parent, mode="indeterminate")
        self._progress.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 10))
        self._progress.grid_remove()  # oculto por padrão

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    def _on_generate(self):
        if self._is_generating:
            return

        prompt = self._prompt_box.get("1.0", "end").strip()
        if not prompt:
            self._set_status("⚠️ Digite uma descrição antes de gerar.", "orange")
            return

        self._is_generating = True
        self._btn_generate.configure(state="disabled", text="⏳ Gerando...")
        self._btn_save.configure(state="disabled")
        self._progress.grid()
        self._progress.start()
        self._set_status("Enviando para Pollinations.ai...", "gray")

        # Executa em thread separada para não travar a UI
        thread = threading.Thread(target=self._generate_worker, args=(prompt,), daemon=True)
        thread.start()

    def _generate_worker(self, prompt: str):
        """Roda em background thread."""
        try:
            style = self._style_var.get()
            size_str = self._size_var.get()
            w, h = map(int, size_str.split("x"))

            if self.art_module:
                result = self.art_module.generate_sprite(
                    prompt=prompt,
                    width=w,
                    height=h,
                    style=style,
                    save_name=None,
                )
                if result["success"] and result.get("image_data"):
                    image_bytes = result["image_data"]
                else:
                    # Fallback: baixar diretamente da URL
                    image_bytes = self._fetch_from_url(result.get("url", ""))
            else:
                # Modo standalone (sem módulo completo)
                from app.services.pollinations_service import PollinationsService
                svc = PollinationsService()
                full_prompt = f"{style}, {prompt}, transparent background, game asset"
                res = svc.generate_image(full_prompt, w, h)
                image_bytes = res.get("image_data") if res["success"] else None
                result = res

            if image_bytes:
                self._current_image = Image.open(io.BytesIO(image_bytes))
                self.after(0, self._update_preview_success)
            else:
                error = result.get("error", "Erro desconhecido")
                self.after(0, lambda: self._update_preview_error(error))

        except Exception as e:
            self.after(0, lambda: self._update_preview_error(str(e)))

    def _fetch_from_url(self, url: str) -> bytes | None:
        """Baixa imagem diretamente de uma URL (fallback)."""
        if not url:
            return None
        import urllib.request
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception:
            return None

    def _update_preview_success(self):
        """Atualiza a UI após geração bem-sucedida (roda na thread principal)."""
        self._progress.stop()
        self._progress.grid_remove()
        self._is_generating = False
        self._btn_generate.configure(state="normal", text="✨ Gerar Sprite")
        self._btn_save.configure(state="normal")
        self._set_status("✅ Sprite gerado com sucesso!", "#2a7a3b")

        # Exibe a imagem
        if self._current_image:
            img = self._current_image.copy()
            img.thumbnail((500, 500), Image.LANCZOS)
            self._tk_image = ImageTk.PhotoImage(img)
            self._image_label.configure(image=self._tk_image, text="")

    def _update_preview_error(self, error: str):
        """Atualiza a UI após falha (roda na thread principal)."""
        self._progress.stop()
        self._progress.grid_remove()
        self._is_generating = False
        self._btn_generate.configure(state="normal", text="✨ Gerar Sprite")
        self._set_status(f"❌ Erro: {error}", "#c0392b")

    def _on_save(self):
        """Salva o sprite gerado em disco."""
        if not self._current_image:
            return

        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            title="Salvar Sprite",
        )
        if file_path:
            self._current_image.save(file_path, "PNG")
            self._set_status(f"💾 Salvo em: {file_path}", "#2a7a3b")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _set_status(self, message: str, color: str = "gray"):
        self._status_label.configure(text=message, text_color=color)

    def set_module(self, art_module) -> None:
        """Injeta o módulo Art Studio após construção."""
        self.art_module = art_module
