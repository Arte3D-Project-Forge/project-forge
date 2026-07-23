from app.core.module import ForgeModule

from app.modules.documents.ui.documents_window import DocumentsWindow



class DocumentsModule(ForgeModule):


    def __init__(self, project_path=None):

        super().__init__(

            module_id="documents",

            name="Documents",

            category="Documentation",

            version="1.0",

            status="Stable"

        )


        self.project_path = project_path

        self.window = None



    def initialize(self):

        return "Documents initialized."



    def open(self):


        self.window = DocumentsWindow(

            project_path=self.project_path

        )


        self.window.focus_force()


        return (

            "Documents UI opened."

        )



    def shutdown(self):


        if self.window:


            try:

                self.window.destroy()


            except Exception:

                pass



            self.window = None



        return (

            "Documents shutdown."

        )