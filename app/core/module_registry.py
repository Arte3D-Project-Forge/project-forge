class ModuleRegistry:
    """
    Central registry for Project Forge modules.

    Responsible for:
    - Registering module instances
    - Listing available modules
    - Finding modules
    - Providing module instances
    """



    def __init__(self):

        self.modules = {}



    def register(self, module):


        info = module.get_info()


        module_id = info["id"]


        self.modules[module_id] = {


            "info": info,

            "instance": module


        }



    def unregister(self, module_id):


        if module_id in self.modules:


            del self.modules[module_id]



    def get_module(self, module_id):


        module = self.modules.get(
            module_id
        )


        if module:

            return module["info"]


        return None



    def get_instance(self, module_id):


        module = self.modules.get(
            module_id
        )


        if module:

            return module["instance"]


        return None



    def get_registered_instances(self):


        return [

            module["instance"]

            for module in self.modules.values()

        ]



    def get_all_modules(self):


        return [

            module["info"]

            for module in self.modules.values()

        ]



    def exists(self, module_id):


        return module_id in self.modules