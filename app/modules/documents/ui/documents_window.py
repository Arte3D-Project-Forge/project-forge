import customtkinter as ctk



class DocumentsWindow(ctk.CTkToplevel):


    def __init__(self, parent=None):

        super().__init__(parent)


        self.title(
            "Documents Module"
        )


        self.geometry(
            "700x450"
        )


        self.create_ui()



    def create_ui(self):


        title = ctk.CTkLabel(
            self,
            text="📄 Documents Manager",
            font=("Arial", 28, "bold")
        )


        title.pack(
            pady=30
        )



        info = ctk.CTkLabel(
            self,
            text="Project Forge Document System",
            font=("Arial", 16)
        )


        info.pack()



        button = ctk.CTkButton(
            self,
            text="Create Document",
            command=self.create_document
        )


        button.pack(
            pady=40
        )



    def create_document(self):


        print(
            "Create document requested"
        )