from app.core.module_registry import ModuleRegistry



class ModuleManager:


    def __init__(self, registry):

        self.registry = registry

        self.loaded_modules = {}



    def initialize_modules(self):


        modules = self.registry.get_all_modules()


        for module in modules:

            self.loaded_modules[
                module["id"]
            ] = {

                "info": module,

                "status": "initialized"

            }



        return True



    def get_modules(self):


        return list(
            self.loaded_modules.values()
        )



    def get_module(self,module_id):


        return self.loaded_modules.get(
            module_id
        )



    def shutdown_modules(self):


        self.loaded_modules.clear()


        return True