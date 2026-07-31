class WorkspaceController:


    def __init__(
        self,
        registry
    ):

        self.registry = registry



    def get_modules(self):

        return self.registry.modules.values()


    def get_available_modules(self):

        return self.registry.get_all_modules()



    def open_module(
        self,
        module_id,
        parent=None
    ):


        module = self.registry.get_module(
            module_id
        )


        if not module:

            return "Module not found."



        return module.open(parent=parent)



    def initialize_modules(self):


        results = []


        for module in self.registry.modules.values():


            results.append(

                module.initialize()

            )


        return results



    def shutdown_modules(self):


        results = []


        for module in self.registry.modules.values():


            results.append(

                module.shutdown()

            )


        return results