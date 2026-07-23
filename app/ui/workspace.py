import customtkinter as ctk



class Workspace(ctk.CTk):


    def __init__(self, modules):

        super().__init__()


        self.modules = modules


        self.title(
            "Project Forge"
        )


        self.geometry(
            "900x600"
        )


        self.build_ui()



    def build_ui(self):


        title = ctk.CTkLabel(

            self,

            text="PROJECT FORGE",

            font=(
                "Arial",
                32,
                "bold"
            )

        )


        title.pack(
            pady=30
        )



        subtitle = ctk.CTkLabel(

            self,

            text="Production Workspace",

            font=(
                "Arial",
                18
            )

        )


        subtitle.pack(
            pady=10
        )



        modules_frame = ctk.CTkFrame(
            self
        )


        modules_frame.pack(

            fill="both",

            expand=True,

            padx=40,

            pady=30

        )



        for module in self.modules:


            self.create_module_card(

                modules_frame,

                module

            )



    def create_module_card(
        self,
        parent,
        module
    ):


        info = module.get_info()



        card = ctk.CTkFrame(

            parent,

            height=120

        )


        card.pack(

            fill="x",

            pady=10

        )



        name = ctk.CTkLabel(

            card,

            text=info["name"],

            font=(

                "Arial",

                20,

                "bold"

            )

        )


        name.pack(

            side="left",

            padx=20

        )



        category = ctk.CTkLabel(

            card,

            text=info["category"]

        )


        category.pack(

            side="left",

            padx=20

        )



        button = ctk.CTkButton(

            card,

            text="OPEN",

            command=lambda:

                module.open()

        )


        button.pack(

            side="right",

            padx=20

        )