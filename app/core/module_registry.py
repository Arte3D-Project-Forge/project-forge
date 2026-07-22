class ModuleRegistry:
    """
    Central registry for Project Forge modules.

    Responsible for:
    - Registering modules
    - Listing available modules
    - Finding modules by ID
    """


    def __init__(self):

        self.modules = {}



    def register(self, module):

        module_id = module["id"]

        self.modules[module_id] = module



    def unregister(self, module_id):

        if module_id in self.modules:

            del self.modules[module_id]



    def get_module(self, module_id):

        return self.modules.get(
            module_id
        )



    def get_all_modules(self):

        return list(
            self.modules.values()
        )



    def exists(self, module_id):

        return module_id in self.modules