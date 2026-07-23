class WorkspaceController:


    def __init__(self, registry):

        self.registry = registry



    def get_available_modules(self):

        return (
            self.registry.get_all_modules()
        )



    def get_module(self, module_id):

        return (
            self.registry.get_module(module_id)
        )