from app.modules.documents.module import DocumentsModule
from app.modules.production.module import ProductionModule



class ModuleLoader:


    def __init__(self, registry):

        self.registry = registry



    def load_modules(self):


        modules = [

            DocumentsModule(),

            ProductionModule()

        ]


        for module in modules:

            self.registry.register(
                module
            )


        return modules