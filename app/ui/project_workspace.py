import customtkinter as ctk


class ProjectWorkspace(ctk.CTkToplevel):

    def __init__(self, parent, project):

        super().__init__(parent)

        self.project = project
        self.modules = {}

        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.lift()

        self.title(
            f"Workspace - {project['name']}"
        )

        self.geometry(
            "1100x700"
        )

        self.create_layout()


    def create_layout(self):

        self.create_header()

        self.create_main_area()

        self.create_status_bar()



    def create_header(self):

        header = ctk.CTkFrame(
            self
        )

        header.pack(
            fill="x",
            padx=10,
            pady=10
        )


        title = ctk.CTkLabel(
            header,
            text=self.project["name"],
            font=(
                "Arial",
                26,
                "bold"
            )
        )

        title.pack(
            side="left",
            padx=20
        )


        engine = ctk.CTkLabel(
            header,
            text=f"Engine: {self.project['engine']}",
            font=(
                "Arial",
                14
            )
        )

        engine.pack(
            side="right",
            padx=20
        )



    def create_main_area(self):

        container = ctk.CTkFrame(
            self
        )

        container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )


        self.sidebar = ctk.CTkFrame(
            container,
            width=220
        )

        self.sidebar.pack(
            side="left",
            fill="y",
            padx=5
        )


        self.content_area = ctk.CTkFrame(
            container
        )

        self.content_area.pack(
            side="right",
            fill="both",
            expand=True,
            padx=5
        )


        self.create_sidebar()

        self.show_welcome()



    def create_sidebar(self):

        title = ctk.CTkLabel(
            self.sidebar,
            text="MODULES",
            font=(
                "Arial",
                18,
                "bold"
            )
        )

        title.pack(
            pady=20
        )


        modules = [

            "Documents",

            "Game Design",

            "Lore",

            "Roadmap",

            "Art Studio",

            "Audio Studio",

            "AI Agents"

        ]


        for module in modules:

            button = ctk.CTkButton(
                self.sidebar,
                text=module,
                height=40,
                command=lambda m=module: self.open_module(m)
            )

            button.pack(
                fill="x",
                padx=15,
                pady=5
            )



    def open_module(self, module_name):

        self.clear_content()


        label = ctk.CTkLabel(
            self.content_area,
            text=(
                module_name
                +
                "\n\nModule ready for integration."
            ),
            font=(
                "Arial",
                20
            )
        )

        label.pack(
            expand=True
        )



    def show_welcome(self):

        self.clear_content()


        label = ctk.CTkLabel(
            self.content_area,
            text=(
                "PROJECT FORGE WORKSPACE\n\n"
                "Select a module"
            ),
            font=(
                "Arial",
                22,
                "bold"
            )
        )

        label.pack(
            expand=True
        )



    def clear_content(self):

        for widget in self.content_area.winfo_children():

            widget.destroy()



    def create_status_bar(self):

        status = ctk.CTkLabel(
            self,
            text="Project Forge | Workspace Release 1.0",
            anchor="w"
        )

        status.pack(
            fill="x",
            padx=10,
            pady=5
        )