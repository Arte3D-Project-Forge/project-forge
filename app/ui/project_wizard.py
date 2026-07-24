import customtkinter as ctk

from app.models.project import Project
from app.services.project_creator import ProjectCreator


class ProjectWizard(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Novo Projeto")
        self.geometry("500x400")

        self.parent = parent

        self.create_ui()


    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Criar Novo Projeto",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=20)


        self.name_entry = ctk.CTkEntry(
            self,
            placeholder_text="Nome do Projeto",
            width=300
        )

        self.name_entry.pack(pady=10)


        self.engine_box = ctk.CTkComboBox(
            self,
            values=[
                "Godot",
                "Unity",
                "Unreal"
            ],
            width=300
        )

        self.engine_box.pack(pady=10)

        self.engine_box.set("Godot")


        create_button = ctk.CTkButton(
            self,
            text="Criar Projeto",
            command=self.create_project
        )

        create_button.pack(pady=30)



    def create_project(self):

        name = self.name_entry.get()
        engine = self.engine_box.get()


        project = Project(
            name,
            engine
        )


        creator = ProjectCreator()

        creator.create(project)


        self.destroy()