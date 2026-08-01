import threading
import webbrowser

import customtkinter as ctk
from tkinter import messagebox

from app.core.config_manager import ConfigManager
from app.ui.forge_view import (
    ACCENT,
    ACCENT_HOVER,
    BG,
    CARD_BG,
    CARD_HOVER,
    MUTED,
    TEXT,
    ForgeView,
    font,
)


class SettingsView(ForgeView):
    """Configurações (frame da janela única)."""

    def __init__(self, master, app=None, project=None):
        super().__init__(master, app=app, project=project)

        self.config = ConfigManager()
        self.comfyui_url = (
            self.config.config.get("comfyui", {})
            .get("server_url", "http://127.0.0.1:8188")
        )

        self.url_var = ctk.StringVar(value=self.comfyui_url)

        self.build_ui()

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
            text="CONFIGURAÇÕES",
            font=font(24, "bold"),
            text_color=TEXT,
        )
        title.pack(side="left", padx=16)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=30, pady=(8, 16))

        # ---- Geração ----
        gen_frame = ctk.CTkFrame(body, fg_color=CARD_BG, corner_radius=12)
        gen_frame.pack(pady=6, fill="x")

        ctk.CTkLabel(
            gen_frame,
            text="⚡ Geração de imagens",
            font=font(15, "bold"),
            text_color=TEXT,
        ).pack(pady=(12, 4), padx=15, anchor="w")

        info = ctk.CTkLabel(
            gen_frame,
            text=(
                "O Forge escolhe o melhor gerador automaticamente:\n"
                "ComfyUI (se detectado) → Pollinations → Stable Horde.\n"
                "Nenhuma configuração é necessária para funcionar."
            ),
            font=font(12),
            text_color=MUTED,
            justify="left",
        )
        info.pack(padx=15, pady=(0, 8), anchor="w")

        # ---- Seletor de provider ativo ----
        provider_row = ctk.CTkFrame(gen_frame, fg_color="transparent")
        provider_row.pack(padx=15, pady=(0, 6), fill="x")

        ctk.CTkLabel(
            provider_row,
            text="Gerador ativo:",
            font=font(12, "bold"),
            text_color=TEXT,
        ).pack(side="left")

        self.provider_var = ctk.StringVar(
            value=self.config.get_image_provider()
        )
        provider_options = self.config.config.get(
            "providers", {}
        ).get("image", {}).get("available", [
            "mock", "openai", "comfyui", "pollinations",
            "huggingface", "stablehorde",
        ])

        self.provider_menu = ctk.CTkOptionMenu(
            provider_row,
            values=provider_options,
            variable=self.provider_var,
            width=190,
            fg_color=BG,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
            font=font(12),
            dropdown_font=font(12),
            command=self._on_provider_change,
        )
        self.provider_menu.pack(side="left", padx=10)

        provider_hint = {
            "comfyui": "Qualidade máxima (Colab + túnel)",
            "stablehorde": "Grátis, rede distribuída (AIO Pixel Art)",
            "pollinations": "Grátis, rápido, bom para testes",
            "huggingface": "Grátis, requer token opcional",
            "openai": "Requer API key",
            "mock": "Teste (quadrado colorido)",
        }
        self.provider_hint_label = ctk.CTkLabel(
            gen_frame,
            text=provider_hint.get(self.provider_var.get(), ""),
            font=font(11),
            text_color=MUTED,
        )
        self.provider_hint_label.pack(padx=15, pady=(0, 10), anchor="w")

        # ---- ComfyUI (avançado) ----
        comfy_frame = ctk.CTkFrame(body, fg_color=CARD_BG, corner_radius=12)
        comfy_frame.pack(pady=6, fill="x")

        ctk.CTkLabel(
            comfy_frame,
            text="🖥️ ComfyUI (opcional / avançado)",
            font=font(15, "bold"),
            text_color=TEXT,
        ).pack(pady=(12, 4), padx=15, anchor="w")

        row = ctk.CTkFrame(comfy_frame, fg_color="transparent")
        row.pack(padx=15, pady=5, fill="x")

        ctk.CTkLabel(row, text="URL do servidor:", font=font(12)).pack(
            side="left", padx=(0, 8)
        )

        self.url_entry = ctk.CTkEntry(
            row,
            textvariable=self.url_var,
            fg_color=BG,
            border_width=0,
            text_color=TEXT,
            font=font(12),
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=5)

        self.url_var.trace_add("write", self._on_url_change)

        btn_test = ctk.CTkButton(
            row,
            text="Testar",
            width=80,
            corner_radius=8,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=self.test_comfyui,
        )
        btn_test.pack(side="left", padx=5)

        self.status = ctk.CTkLabel(
            comfy_frame,
            text="",
            font=font(12),
        )
        self.status.pack(pady=(0, 4))

        colab = ctk.CTkButton(
            comfy_frame,
            text="🎓 Como gerar de graça com qualidade máxima (notebook Colab)",
            corner_radius=8,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=self.open_colab,
        )
        colab.pack(pady=(0, 14), padx=15)

        # ---- Sincronização automática ----
        sync_frame = ctk.CTkFrame(body, fg_color=CARD_BG, corner_radius=12)
        sync_frame.pack(pady=6, fill="x")

        ctk.CTkLabel(
            sync_frame,
            text="🔄 Sincronização automática do túnel",
            font=font(15, "bold"),
            text_color=TEXT,
        ).pack(pady=(12, 2), padx=15, anchor="w")

        self.sync_var = ctk.StringVar(
            value=self.config.config.get("comfyui", {}).get("sync_url", "")
        )

        sync_row = ctk.CTkFrame(sync_frame, fg_color="transparent")
        sync_row.pack(padx=15, pady=4, fill="x")

        self.sync_entry = ctk.CTkEntry(
            sync_row,
            textvariable=self.sync_var,
            state="readonly",
            fg_color=BG,
            border_width=0,
            text_color=MUTED,
            font=font(11),
        )
        self.sync_entry.pack(side="left", fill="x", expand=True, padx=5)

        btn_sync = ctk.CTkButton(
            sync_row,
            text="Criar link",
            width=90,
            corner_radius=8,
            fg_color=CARD_BG,
            hover_color=CARD_HOVER,
            command=self.create_sync_link,
        )
        btn_sync.pack(side="left", padx=5)

        self.sync_status = ctk.CTkLabel(
            sync_frame,
            text=(
                "Já configurado automaticamente. Quando o notebook do "
                "Colab estiver rodando, o Forge descobre a URL sozinho."
            ),
            font=font(11),
            text_color=MUTED,
            wraplength=520,
            justify="left",
        )
        self.sync_status.pack(pady=(0, 12), padx=15, anchor="w")

        # ---- Sobre ----
        about = ctk.CTkLabel(
            body,
            text=(
                "Project Forge v1.0\n"
                "AI Game Development Operating System"
            ),
            font=font(11),
            text_color=MUTED,
        )
        about.pack(pady=10)

    # ==========================
    # AÇÕES
    # ==========================

    def _on_provider_change(self, name):
        image_cfg = self.config.config.get("providers", {}).get("image", {})
        image_cfg["active"] = name
        self.config.set("providers", "image", image_cfg)

        hints = {
            "comfyui": "Qualidade máxima (Colab + túnel)",
            "stablehorde": "Grátis, rede distribuída (AIO Pixel Art)",
            "pollinations": "Grátis, rápido, bom para testes",
            "huggingface": "Grátis, requer token opcional",
            "openai": "Requer API key",
            "mock": "Teste (quadrado colorido)",
        }
        self.provider_hint_label.configure(
            text=hints.get(name, "")
        )

    def _on_url_change(self, *args):
        url = self.url_entry.get().strip().rstrip("/")

        if url.startswith("http") and url != self.comfyui_url:
            self.config.set("comfyui", "server_url", url)
            self.comfyui_url = url
            self.status.configure(
                text="URL salva automaticamente. Clique em Testar.",
                text_color="orange",
            )

    def test_comfyui(self):
        url = self.url_entry.get().strip().rstrip("/")

        if not url:
            messagebox.showwarning(
                "Configurações",
                "Digite a URL do servidor ComfyUI.",
            )
            return

        self.config.set("comfyui", "server_url", url)
        self.comfyui_url = url

        self.status.configure(
            text="Testando conexão...",
            text_color="orange",
        )

        def do_test():
            import ssl
            import urllib.request

            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            ok = False
            try:
                req = urllib.request.Request(f"{url}/system_stats")
                urllib.request.urlopen(req, timeout=10, context=context)
                ok = True
            except Exception:
                ok = False

            def update():
                if ok:
                    self.status.configure(
                        text="CONECTADO — o Forge passará a usar o ComfyUI.",
                        text_color="green",
                    )
                else:
                    self.status.configure(
                        text=(
                            "URL salva, mas OFFLINE — verifique se o "
                            "túnel do Colab continua ativo."
                        ),
                        text_color="red",
                    )

            self.after(0, update)

        threading.Thread(target=do_test, daemon=True).start()

    def open_colab(self):
        url = (
            self.config.config
            .get("comfyui", {})
            .get(
                "colab_url",
                "https://colab.research.google.com/github/"
                "Arte3D-Project-Forge/project-forge/blob/main/"
                "colab/ComfyUI_Forge_Notebook.ipynb",
            )
        )

        webbrowser.open(url)

        self.status.configure(
            text=(
                "Notebook aberto. Depois de gerar a URL do túnel, "
                "cole-a no campo acima e clique em Testar."
            ),
            text_color="white",
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
                        text_color="red",
                    ),
                )
                return

            def update():
                self.config.set("comfyui", "sync_url", link)
                self.sync_var.set(link)
                self.sync_entry.configure(state="normal")
                self.sync_entry.select_range(0, "end")
                top = self.winfo_toplevel()
                top.clipboard_clear()
                top.clipboard_append(link)
                self.sync_entry.configure(state="readonly")
                self.sync_status.configure(
                    text=(
                        "Link copiado! Cole na célula 'Túnel automático' "
                        "do Colab e rode. O Forge descobrirá a URL sozinho."
                    ),
                    text_color="green",
                )

            self.after(0, update)

        self.sync_status.configure(
            text="Criando link de sincronização...",
            text_color="orange",
        )

        threading.Thread(target=do_create, daemon=True).start()


class SettingsWindow(ctk.CTkToplevel):
    """Wrapper legado: abre configurações em janela própria."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.title("Configurações")
        self.geometry("620x700")

        self.lift()
        self.focus_force()

        view = SettingsView(self, app=None)
        view.pack(fill="both", expand=True)
