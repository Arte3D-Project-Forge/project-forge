from app.modules.documents.module import DocumentsModule
from app.modules.production.module import ProductionModule



class ModuleLoader:


    def __init__(self, registry):

        self.registry = registry



    def __init__(self, registry, project=None):

        self.registry = registry
        self.project = project


    def load_modules(self):


        modules = [

            DocumentsModule(
                project_path=self.project["path"]
            ),

            ProductionModule(
                project=self.project
            )

        ]


        for module in modules:

            self.registry.register(
                module
            )


        return modules