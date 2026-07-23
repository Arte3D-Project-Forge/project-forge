from app.core.module import ForgeModule

from app.modules.production.ui.production_window import ProductionWindow



class ProductionModule(ForgeModule):


    def __init__(self):

        super().__init__(

            module_id="production",

            name="Production",

            category="Creation",

            version="1.0",

            status="Stable"

        )


        self.window = None



    def initialize(self):

        return "Production initialized."



    def open(self):


        self.window = ProductionWindow()


        self.window.focus_force()


        return (
            "Production UI opened."
        )



    def shutdown(self):


        if self.window:


            self.window.destroy()


            self.window = None



        return (
            "Production shutdown."
        )