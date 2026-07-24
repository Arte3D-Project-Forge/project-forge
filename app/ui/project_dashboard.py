import customtkinter as ctk

from app.services.project_manager import ProjectManager
from app.ui.project_workspace import ProjectWorkspace


class ProjectDashboard(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.lift()

        self.title("Projetos")
        self.geometry("600x500")

        self.manager = ProjectManager()

        self.create_ui()


    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Projetos Recentes",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=20)


        projects = self.manager.load_projects()


        if not projects:

            label = ctk.CTkLabel(
                self,
                text="Nenhum projeto encontrado"
            )

            label.pack(pady=20)

            return


        for project in projects:


            frame = ctk.CTkFrame(self)

            frame.pack(
                pady=10,
                padx=20,
                fill="x"
            )


            name = ctk.CTkButton(
                frame,
                text=project["name"],
                font=("Arial", 18, "bold"),
                command=lambda p=project: self.open_project(p)
            )

            name.pack(pady=5)


            engine = ctk.CTkLabel(
                frame,
                text=f"Engine: {project['engine']}"
            )

            engine.pack()


            path = ctk.CTkLabel(
                frame,
                text=project["path"]
            )

            path.pack(pady=5)



    def open_project(self, project):

        print("Abrindo projeto:", project["name"])


        workspace = ProjectWorkspace(
            self,
            project
        )

        workspace.focus()