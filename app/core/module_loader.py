from app.modules.documents.module import DocumentsModule



class ModuleLoader:


    def __init__(self, registry):

        self.registry = registry



    def load_modules(self):


        modules = [

            DocumentsModule()

        ]



        for module in modules:


            self.registry.register(
                module
            )



        return modules