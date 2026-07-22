import customtkinter as ctk


class ArtStudio(ctk.CTkToplevel):

    def __init__(self, parent, project):

        super().__init__(parent)


        self.project = project


        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.lift()


        self.title(
            f"Art Studio - {project['name']}"
        )


        self.geometry("800x600")


        self.create_ui()



    def create_ui(self):


        title = ctk.CTkLabel(
            self,
            text="🎨 Art Studio",
            font=("Arial", 32, "bold")
        )

        title.pack(
            pady=20
        )



        project = ctk.CTkLabel(
            self,
            text=self.project["name"],
            font=("Arial", 18)
        )

        project.pack()



        subtitle = ctk.CTkLabel(
            self,
            text="Gerenciamento de Arte do Projeto",
            font=("Arial", 16)
        )

        subtitle.pack(
            pady=20
        )



        frame = ctk.CTkFrame(
            self
        )

        frame.pack(
            padx=40,
            pady=20,
            fill="both",
            expand=True
        )



        modules = [

            "🧍 Characters",

            "🌲 Environment",

            "🧱 Tiles",

            "⚔ Items",

            "✨ Effects",

            "🤖 AI Image Pipeline"

        ]



        for module in modules:


            button = ctk.CTkButton(
                frame,
                text=module,
                height=45
            )


            button.pack(
                pady=8,
                padx=80,
                fill="x"
            )