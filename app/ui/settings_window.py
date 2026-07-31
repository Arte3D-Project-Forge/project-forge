import threading
import webbrowser

import customtkinter as ctk
from tkinter import messagebox

from app.core.config_manager import ConfigManager


class SettingsWindow(ctk.CTkToplevel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.config = ConfigManager()
        self.comfyui_url = (
            self.config.config.get("comfyui", {})
            .get("server_url", "http://127.0.0.1:8188")
        )

        self.url_var = ctk.StringVar(
            value=self.comfyui_url
        )

        self.title("Configurações")
        self.geometry("560x420")

        self.lift()
        self.focus_force()

        self.create_ui()

    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="CONFIGURAÇÕES",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(20, 15))

        # ---- Geração ----
        gen_frame = ctk.CTkFrame(self)
        gen_frame.pack(pady=8, padx=30, fill="x")

        ctk.CTkLabel(
            gen_frame,
            text="Geração de imagens",
            font=("Arial", 15, "bold")
        ).pack(pady=(12, 4), padx=15, anchor="w")

        info = ctk.CTkLabel(
            gen_frame,
            text=(
                "O Forge escolhe o melhor gerador automaticamente:\n"
                "ComfyUI (se detectado no seu PC) → Pollinations → HuggingFace.\n"
                "Nenhuma configuração é necessária para funcionar."
            ),
            font=("Arial", 12),
            text_color="gray",
            justify="left"
        )
        info.pack(padx=15, pady=(0, 12), anchor="w")

        # ---- ComfyUI (avançado) ----
        comfy_frame = ctk.CTkFrame(self)
        comfy_frame.pack(pady=8, padx=30, fill="x")

        ctk.CTkLabel(
            comfy_frame,
            text="ComfyUI (opcional / avançado)",
            font=("Arial", 15, "bold")
        ).pack(pady=(12, 4), padx=15, anchor="w")

        row = ctk.CTkFrame(
            comfy_frame,
            fg_color="transparent"
        )
        row.pack(padx=15, pady=5, fill="x")

        ctk.CTkLabel(
            row,
            text="URL do servidor:"
        ).pack(side="left", padx=(0, 8))

        self.url_entry = ctk.CTkEntry(
            row,
            textvariable=self.url_var
        )
        self.url_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        self.url_var.trace_add(
            "write",
            self._on_url_change
        )

        btn_test = ctk.CTkButton(
            row,
            text="Testar",
            width=80,
            command=self.test_comfyui
        )
        btn_test.pack(side="left", padx=5)

        self.status = ctk.CTkLabel(
            comfy_frame,
            text="",
            font=("Arial", 12)
        )
        self.status.pack(pady=(0, 4))

        colab = ctk.CTkButton(
            comfy_frame,
            text="Como gerar de graça com qualidade máxima (notebook Colab)",
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            command=self.open_colab
        )
        colab.pack(pady=(0, 14), padx=15)

        # ---- Sincronização automática ----
        sync_frame = ctk.CTkFrame(self)
        sync_frame.pack(pady=8, padx=30, fill="x")

        ctk.CTkLabel(
            sync_frame,
            text="Sincronização automática do túnel",
            font=("Arial", 15, "bold")
        ).pack(pady=(12, 2), padx=15, anchor="w")

        self.sync_var = ctk.StringVar(
            value=self.config.config.get(
                "comfyui", {}
            ).get("sync_url", "")
        )

        sync_row = ctk.CTkFrame(
            sync_frame,
            fg_color="transparent"
        )
        sync_row.pack(padx=15, pady=4, fill="x")

        self.sync_entry = ctk.CTkEntry(
            sync_row,
            textvariable=self.sync_var,
            state="readonly"
        )
        self.sync_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        btn_sync = ctk.CTkButton(
            sync_row,
            text="Criar link",
            width=90,
            command=self.create_sync_link
        )
        btn_sync.pack(side="left", padx=5)

        self.sync_status = ctk.CTkLabel(
            sync_frame,
            text=(
                "Cole este link na célula 'Túnel automático' do Colab. "
                "Depois disso, o Forge descobre a URL sozinho."
            ),
            font=("Arial", 11),
            text_color="gray",
            wraplength=470,
            justify="left"
        )
        self.sync_status.pack(pady=(0, 10), padx=15, anchor="w")

        # ---- Sobre ----
        about = ctk.CTkLabel(
            self,
            text=(
                "Project Forge v1.0\n"
                "AI Game Development Operating System"
            ),
            font=("Arial", 11),
            text_color="gray"
        )
        about.pack(pady=10)

    # ==========================
    # AÇÕES
    # ==========================

    def _on_url_change(self, *args):

        url = self.url_entry.get().strip().rstrip("/")

        if url.startswith("http") and url != self.comfyui_url:
            self.config.set(
                "comfyui",
                "server_url",
                url
            )
            self.comfyui_url = url
            self.status.configure(
                text="URL salva automaticamente. Clique em Testar.",
                text_color="orange"
            )

    def test_comfyui(self):

        url = self.url_entry.get().strip().rstrip("/")

        if not url:
            messagebox.showwarning(
                "Configurações",
                "Digite a URL do servidor ComfyUI."
            )
            return

        self.config.set(
            "comfyui",
            "server_url",
            url
        )
        self.comfyui_url = url

        self.status.configure(
            text="Testando conexão...",
            text_color="orange"
        )

        def do_test():

            import ssl
            import urllib.request

            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            ok = False
            try:
                req = urllib.request.Request(
                    f"{url}/system_stats"
                )
                urllib.request.urlopen(
                    req,
                    timeout=10,
                    context=context
                )
                ok = True
            except Exception:
                ok = False

            def update():
                if ok:
                    self.status.configure(
                        text="CONECTADO — o Forge passará a usar o ComfyUI.",
                        text_color="green"
                    )
                else:
                    self.status.configure(
                        text=(
                            "URL salva, mas OFFLINE — verifique se o "
                            "túnel do Colab continua ativo."
                        ),
                        text_color="red"
                    )

            self.after(0, update)

        threading.Thread(
            target=do_test,
            daemon=True
        ).start()

    def open_colab(self):

        url = (
            self.config.config
            .get("comfyui", {})
            .get(
                "colab_url",
                "https://colab.research.google.com/github/"
                "Arte3D-Project-Forge/project-forge/blob/main/"
                "colab/ComfyUI_Forge_Notebook.ipynb"
            )
        )

        webbrowser.open(url)

        self.status.configure(
            text=(
                "Notebook aberto. Depois de gerar a URL do túnel, "
                "cole-a no campo acima e clique em Testar."
            ),
            text_color="white"
        )

    def create_sync_link(self):

        from app.services.comfyui_sync import ComfyUISync

        def do_create():
            try:
                link = ComfyUISync.create_link()
            except Exception as exc:
                self.after(
                    0,
                    lambda: self.sync_status.configure(
                        text=f"Erro ao criar link: {exc}",
                        text_color="red"
                    )
                )
                return

            def update():
                self.config.set(
                    "comfyui",
                    "sync_url",
                    link
                )
                self.sync_var.set(link)
                self.sync_entry.configure(
                    state="normal"
                )
                self.sync_entry.select_range(
                    0, "end"
                )
                self.clipboard_clear()
                self.clipboard_append(link)
                self.sync_entry.configure(
                    state="readonly"
                )
                self.sync_status.configure(
                    text=(
                        "Link copiado! Cole na célula 'Túnel automático' "
                        "do Colab e rode. O Forge descobrirá a URL sozinho."
                    ),
                    text_color="green"
                )

            self.after(0, update)

        self.sync_status.configure(
            text="Criando link de sincronização...",
            text_color="orange"
        )

        threading.Thread(
            target=do_create,
            daemon=True
        ).start()
