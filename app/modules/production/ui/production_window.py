import customtkinter as ctk
from tkinter import messagebox

from app.production.production_job import ProductionJob


class ProductionWindow(ctk.CTkToplevel):


    def __init__(self, project=None):

        super().__init__()


        self.project = project or {

            "name": "Forge_Test_02",

            "engine": "Godot",

            "path": "Forge_Test_02"

        }


        self.title(
            "Forge Production Studio"
        )


        self.geometry(
            "700x550"
        )


        self.build_ui()



    def build_ui(self):


        title = ctk.CTkLabel(

            self,

            text="FORGE PRODUCTION STUDIO",

            font=("Arial", 26, "bold")

        )

        title.pack(
            pady=20
        )


        subtitle = ctk.CTkLabel(

            self,

            text="Descreva o que deseja criar"

        )

        subtitle.pack()



        self.prompt = ctk.CTkTextbox(

            self,

            width=600,

            height=180

        )

        self.prompt.pack(

            pady=20

        )


        button = ctk.CTkButton(

            self,

            text="CRIAR JOB",

            command=self.create_job

        )


        button.pack(

            pady=15

        )


        self.status = ctk.CTkLabel(

            self,

            text="Aguardando produção..."

        )


        self.status.pack()



    def create_job(self):


        request = self.prompt.get(

            "1.0",

            "end"

        ).strip()



        if not request:


            messagebox.showwarning(

                "Forge",

                "Digite o que deseja criar."

            )


            return



        job = ProductionJob(

            self.project,

            request,

            [

                "lore",

                "sprites",

                "animation",

                "tiles"

            ]

        )


        path = job.save()



        self.status.configure(

            text=f"JOB criado:\n{path}"

        )