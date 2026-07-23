import customtkinter as ctk
from tkinter import messagebox

from app.production.production_job import ProductionJob


class ProductionDashboard(ctk.CTkToplevel):

    def __init__(self, parent, project):

        super().__init__(parent)

        self.project = project

        self.title("Forge Production")

        self.geometry("700x500")

        self.build_ui()


    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="PROJECT FORGE",
            font=("Arial", 28, "bold")
        )

        title.pack(pady=20)


        subtitle = ctk.CTkLabel(
            self,
            text="O que você quer criar hoje?",
            font=("Arial", 18)
        )

        subtitle.pack(pady=10)


        self.prompt = ctk.CTkTextbox(
            self,
            width=600,
            height=180
        )

        self.prompt.pack(pady=20)


        button = ctk.CTkButton(
            self,
            text="INICIAR PRODUÇÃO",
            command=self.start_production,
            height=45
        )

        button.pack(pady=20)


        self.status = ctk.CTkLabel(
            self,
            text="Aguardando produção..."
        )

        self.status.pack()


    def start_production(self):

        request = self.prompt.get(
            "1.0",
            "end"
        ).strip()


        if not request:

            messagebox.showwarning(
                "Forge",
                "Descreva o que deseja produzir."
            )

            return


        job = ProductionJob(

            self.project,

            request,

            [

                "lore",

                "sprites",

                "tiles"

            ]

        )


        path = job.save()


        self.status.configure(

            text=f"Job criado:\n{path}"

        )