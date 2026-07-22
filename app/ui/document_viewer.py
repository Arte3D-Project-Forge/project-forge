import customtkinter as ctk
import os


class DocumentViewer(ctk.CTkToplevel):

    def __init__(self, parent, title, file_path):

        super().__init__(parent)


        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.lift()


        self.file_path = file_path


        self.title(title)

        self.geometry("800x600")


        self.create_ui()



    def create_ui(self):


        header = ctk.CTkLabel(
            self,
            text=os.path.basename(self.file_path),
            font=("Arial", 24, "bold")
        )

        header.pack(pady=20)



        self.textbox = ctk.CTkTextbox(
            self,
            width=700,
            height=450
        )

        self.textbox.pack(
            padx=40,
            pady=20,
            fill="both",
            expand=True
        )



        self.load_file()



    def load_file(self):


        if os.path.exists(self.file_path):

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()


        else:

            content = "Documento ainda não criado."


        self.textbox.insert(
            "0.0",
            content
        )