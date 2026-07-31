from app.core.module import ForgeModule

from app.modules.production.ui.production_window import ProductionWindow



class ProductionModule(ForgeModule):


    def __init__(self, project=None):

        super().__init__(

            module_id="production",

            name="Production",

            category="Creation",

            version="1.0",

            status="Stable"

        )


        self.project = project
        self.window = None



    def initialize(self):

        return "Production initialized."



    def open(self, parent=None):


        self.window = ProductionWindow(
            parent=parent,
            project=self.project
        )


        self.window.focus_force()


        return (
            "Production UI opened."
        )



    def shutdown(self):


        if self.window:


            self.window.destroy()


        self.project = None
        self.window = None



        return (
            "Production shutdown."
        )