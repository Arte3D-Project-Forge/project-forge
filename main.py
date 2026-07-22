import customtkinter as ctk

from app.ui.project_wizard import ProjectWizard


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ForgeApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Project Forge")
        self.geometry("900x600")

        self.create_ui()


    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="PROJECT FORGE",
            font=("Arial", 32, "bold")
        )

        title.pack(pady=40)


        subtitle = ctk.CTkLabel(
            self,
            text="AI Game Development Operating System",
            font=("Arial", 16)
        )

        subtitle.pack(pady=10)


        btn_new = ctk.CTkButton(
            self,
            text="Novo Projeto",
            command=self.new_project
        )

        btn_new.pack(pady=10)


        btn_open = ctk.CTkButton(
            self,
            text="Abrir Projeto",
            command=self.open_project
        )

        btn_open.pack(pady=10)


        btn_settings = ctk.CTkButton(
            self,
            text="Configurações",
            command=self.settings
        )

        btn_settings.pack(pady=10)


        btn_exit = ctk.CTkButton(
            self,
            text="Sair",
            command=self.destroy
        )

        btn_exit.pack(pady=40)



    def new_project(self):

        wizard = ProjectWizard(self)

        wizard.focus()



    def open_project(self):

        print("Abrir Projeto")



    def settings(self):

        print("Configurações")



def main():

    app = ForgeApp()

    app.mainloop()