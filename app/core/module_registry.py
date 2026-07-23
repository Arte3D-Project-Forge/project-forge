class ModuleRegistry:


    def __init__(self):

        self.modules = {}



    def register(
        self,
        module
    ):


        info = module.get_info()


        module_id = info["id"]


        self.modules[module_id] = module



    def unregister(
        self,
        module_id
    ):


        if module_id in self.modules:

            del self.modules[module_id]



    def get_module(
        self,
        module_id
    ):


        return self.modules.get(
            module_id
        )



    def get_all_modules(self):


        return [

            module.get_info()

            for module in self.modules.values()

        ]



    def exists(
        self,
        module_id
    ):


        return module_id in self.modules