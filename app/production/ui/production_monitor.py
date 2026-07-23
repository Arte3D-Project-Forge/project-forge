import customtkinter as ctk

from app.production.production_queue import ProductionQueue


class ProductionMonitor(ctk.CTkToplevel):


    def __init__(self, parent, project):

        super().__init__(parent)


        self.project = project

        self.queue = ProductionQueue(
            project
        )


        self.title(
            "Forge Production Queue"
        )


        self.geometry(
            "700x500"
        )


        self.build_ui()


    def build_ui(self):


        title = ctk.CTkLabel(

            self,

            text="PRODUCTION QUEUE",

            font=("Arial", 28, "bold")

        )

        title.pack(
            pady=20
        )


        self.jobs_label = ctk.CTkLabel(

            self,

            text=""

        )

        self.jobs_label.pack(
            pady=20
        )


        refresh = ctk.CTkButton(

            self,

            text="ATUALIZAR",

            command=self.refresh

        )

        refresh.pack(
            pady=10
        )


        self.refresh()



    def refresh(self):


        jobs = self.queue.get_jobs()


        text = (
            f"Jobs encontrados: {len(jobs)}\n\n"
        )


        for index, job in enumerate(
            jobs,
            start=1
        ):


            text += (

                f"{index}. "
                f"{job.get('request')}\n"
                f"Status: "
                f"{job.get('status')}\n\n"

            )


        self.jobs_label.configure(

            text=text

        )