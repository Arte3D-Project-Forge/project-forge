"""
Project Forge — Art Studio
Arquivo de entrada para testar o módulo isoladamente.
Execute: python run_art_studio.py
"""

import sys
import os

# Garante que os imports funcionem a partir da raiz do projeto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from app.modules.art_studio.art_studio_module import ArtStudioModule
from app.ui.panels.art_studio_panel import ArtStudioPanel


def main():
    # Configuração visual do CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Janela principal
    root = ctk.CTk()
    root.title("Project Forge — Art Studio v1.0")
    root.geometry("1100x700")
    root.minsize(900, 600)

    # Inicializa o módulo com pasta local de saída
    output_dir = os.path.join(os.path.dirname(__file__), "output_project")
    module = ArtStudioModule(project_path=output_dir)

    # Cria e exibe o painel
    panel = ArtStudioPanel(root, art_module=module)
    panel.pack(fill="both", expand=True, padx=5, pady=5)

    print("[Project Forge] Art Studio iniciado.")
    print(f"[Project Forge] Sprites serão salvos em: {output_dir}/assets/sprites/")

    root.mainloop()


if __name__ == "__main__":
    main()
