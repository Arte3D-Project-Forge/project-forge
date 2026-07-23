from app.core.module_manager import ModuleManager



class WorkspaceController:


    def __init__(self, registry):

        self.registry = registry


        self.module_manager = ModuleManager(
            registry
        )


    def initialize(self):


        return (
            self.module_manager
            .initialize_modules()
        )



    def get_available_modules(self):


        return (
            self.registry
            .get_all_modules()
        )



    def get_module(self, module_id):


        return (
            self.registry
            .get_module(module_id)
        )



    def open_module(self, module_id):


        module = (
            self.module_manager
            .get_module(module_id)
        )


        if not module:

            return (
                "Module not found"
            )



        return (
            f"Opening module: {module_id}"
        )



    def shutdown(self):


        return (
            self.module_manager
            .shutdown_modules()
        )