import customtkinter as ctk
import os

from app.ui.document_viewer import DocumentViewer


class ProjectWorkspace(ctk.CTkToplevel):

    def __init__(self, parent, project):

        super().__init__(parent)


        self.project = project

        self.viewer = None


        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.lift()


        self.title(
            f"Workspace - {project['name']}"
        )


        self.geometry("900x600")


        self.create_ui()



    def create_ui(self):


        header = ctk.CTkLabel(
            self,
            text=self.project["name"],
            font=("Arial", 32, "bold")
        )

        header.pack(pady=20)



        engine = ctk.CTkLabel(
            self,
            text=f"Engine: {self.project['engine']}",
            font=("Arial", 18)
        )

        engine.pack()



        title = ctk.CTkLabel(
            self,
            text="MÓDULOS DO PROJETO",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=30)



        frame = ctk.CTkFrame(self)

        frame.pack(
            padx=40,
            pady=10,
            fill="both",
            expand=True
        )



        modules = [

            ("📄 Game Design", self.open_game_design),

            ("📜 Lore", self.open_lore),

            ("🗺 Roadmap", self.open_roadmap),

            ("🎨 Art Studio", self.open_art_studio),

            ("🎵 Audio Studio", self.not_ready),

            ("🤖 AI Agents", self.not_ready),

            ("⚙ Tools", self.not_ready)

        ]



        for text, command in modules:


            button = ctk.CTkButton(
                frame,
                text=text,
                height=45,
                command=command
            )


            button.pack(
                pady=8,
                padx=80,
                fill="x"
            )



    def open_game_design(self):


        path = os.path.join(
            self.project["path"],
            "docs",
            "GAME_DESIGN.md"
        )


        self.viewer = DocumentViewer(
            self,
            "Game Design",
            path
        )


        self.viewer.focus()



    def open_lore(self):


        path = os.path.join(
            self.project["path"],
            "docs",
            "LORE.md"
        )


        self.viewer = DocumentViewer(
            self,
            "Lore",
            path
        )


        self.viewer.focus()



    def open_roadmap(self):


        path = os.path.join(
            self.project["path"],
            "docs",
            "ROADMAP.md"
        )


        self.viewer = DocumentViewer(
            self,
            "Roadmap",
            path
        )


        self.viewer.focus()



    def not_ready(self):

        print(
            "Módulo em desenvolvimento"
        )