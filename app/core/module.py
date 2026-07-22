class ForgeModule:


    def __init__(
        self,
        module_id,
        name,
        category,
        version="1.0",
        status="Stable"
    ):

        self.info = {

            "id": module_id,

            "name": name,

            "category": category,

            "version": version,

            "status": status

        }



    def get_info(self):

        return self.info



    def initialize(self):

        return (
            f"{self.info['name']} initialized."
        )



    def shutdown(self):

        return (
            f"{self.info['name']} shutdown."
        )