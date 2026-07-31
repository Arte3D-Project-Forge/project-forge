import customtkinter as ctk
import os

from app.ui.document_viewer import DocumentViewer
from app.ui.sprite_viewer import SpriteViewer

from app.core.workspace_controller import WorkspaceController
from app.core.module_registry import ModuleRegistry
from app.core.module_loader import ModuleLoader



class ProjectWorkspace(ctk.CTkToplevel):


    def __init__(self, parent, project):

        super().__init__(parent)


        self.project = project

        self.viewer = None


        self.after(50, self._show_on_top)


        self.title(
            f"Workspace - {project['name']}"
        )


        self.geometry(
            "1000x700"
        )


        self.setup_modules()

        self.create_ui()


    def _show_on_top(self):
        self.lift()
        self.focus_force()


    # ==========================
    # MODULE SYSTEM
    # ==========================

    def setup_modules(self):


        self.registry = ModuleRegistry()


        self.loader = ModuleLoader(
            self.registry,
            project=self.project
        )


        self.loader.load_modules()


        self.controller = WorkspaceController(
            self.registry
        )



    # ==========================
    # UI
    # ==========================

    def create_ui(self):


        header = ctk.CTkLabel(
            self,
            text=self.project["name"],
            font=("Arial",32,"bold")
        )


        header.pack(
            pady=20
        )



        engine = ctk.CTkLabel(
            self,
            text=f"Engine: {self.project['engine']}",
            font=("Arial",18)
        )


        engine.pack()



        container = ctk.CTkFrame(
            self
        )


        container.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=30
        )


        self.create_modules_section(
            container
        )


        self.create_documents_section(
            container
        )


        self.create_gallery_button(
            container
        )



    # ==========================
    # MODULES
    # ==========================

    def create_modules_section(self,parent):


        title = ctk.CTkLabel(
            parent,
            text="PROJECT MODULES",
            font=("Arial",20,"bold")
        )


        title.pack(
            pady=10
        )



        modules = (
            self.controller
            .get_available_modules()
        )


        for module in modules:


            button = ctk.CTkButton(
                parent,
                text=module["name"],
                height=45,
                command=lambda m=module:
                    self.open_module(m)
            )


            button.pack(
                fill="x",
                padx=80,
                pady=5
            )



    def open_module(self,module):

        self.controller.open_module(
            module["id"],
            parent=self
        )



    # ==========================
    # DOCUMENTS
    # ==========================

    def create_documents_section(self,parent):


        title = ctk.CTkLabel(
            parent,
            text="PROJECT DOCUMENTS",
            font=("Arial",20,"bold")
        )


        title.pack(
            pady=(30,10)
        )



        documents = [

            (
                "Game Design",
                self.open_game_design
            ),

            (
                "Lore",
                self.open_lore
            ),

            (
                "Roadmap",
                self.open_roadmap
            )

        ]



        for text,command in documents:


            button = ctk.CTkButton(
                parent,
                text=text,
                height=40,
                command=command
            )


            button.pack(
                fill="x",
                padx=80,
                pady=5
            )



    # ==========================
    # DOCUMENT VIEWER
    # ==========================

    def open_game_design(self):


        self.open_document(
            "Game Design",
            "GAME_DESIGN.md"
        )



    def open_lore(self):


        self.open_document(
            "Lore",
            "LORE.md"
        )



    def open_roadmap(self):


        self.open_document(
            "Roadmap",
            "ROADMAP.md"
        )



    def open_document(self,title,file):


        path = os.path.join(
            self.project["path"],
            "docs",
            file
        )


        self.viewer = DocumentViewer(
            self,
            title,
            path
        )


        self.viewer.focus()


    def create_gallery_button(self, parent):

        title = ctk.CTkLabel(
            parent,
            text="GALERIA DE ARTE",
            font=("Arial", 20, "bold")
        )

        title.pack(
            pady=(30, 10)
        )

        button = ctk.CTkButton(
            parent,
            text="Sprite Gallery",
            height=40,
            fg_color="green",
            hover_color="darkgreen",
            command=self.open_sprite_gallery
        )

        button.pack(
            fill="x",
            padx=80,
            pady=5
        )


    def open_sprite_gallery(self):

        viewer = SpriteViewer(
            self,
            self.project
        )

        viewer.focus()