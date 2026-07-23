from app.core.module import ForgeModule

from app.modules.documents.ui.documents_window import DocumentsWindow



class DocumentsModule(ForgeModule):


    def __init__(self):

        super().__init__(

            module_id="documents",

            name="Documents",

            category="Documentation",

            version="1.0",

            status="Stable"

        )


        self.window = None



    def initialize(self):

        return "Documents initialized."



    def open(self):


        self.window = DocumentsWindow()


        self.window.focus_force()


        return (
            "Documents UI opened."
        )



    def shutdown(self):


        if self.window:


            self.window.destroy()


            self.window = None



        return (
            "Documents shutdown."
        )