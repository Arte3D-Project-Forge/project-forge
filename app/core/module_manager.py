from app.core.module_registry import ModuleRegistry



class ModuleManager:


    def __init__(self, registry):

        self.registry = registry

        self.loaded_modules = {}



    def initialize_modules(self):


        modules = self.registry.get_registered_instances()


        for module in modules:


            info = module.get_info()


            module.initialize()



            self.loaded_modules[
                info["id"]
            ] = {


                "info": info,

                "instance": module,

                "status": "initialized"


            }



        return True



    def get_modules(self):


        return list(
            self.loaded_modules.values()
        )



    def get_module(self, module_id):


        return self.loaded_modules.get(
            module_id
        )



    def open_module(self, module_id):


        module_data = self.get_module(
            module_id
        )


        if not module_data:


            return "Module not found"



        module = module_data[
            "instance"
        ]


        return module.open()



    def shutdown_modules(self):


        for module_data in self.loaded_modules.values():


            module = module_data[
                "instance"
            ]


            module.shutdown()



        self.loaded_modules.clear()


        return True