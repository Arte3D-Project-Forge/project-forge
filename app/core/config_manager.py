import json
import os



class ConfigManager:


    def __init__(
        self,
        config_path="config/forge_config.json"
    ):


        self.config_path = config_path

        self.config = self.load()



    def load(
        self
    ):


        if not os.path.exists(

            self.config_path

        ):

            raise FileNotFoundError(

                "Forge configuration not found"

            )


        with open(

            self.config_path,

            "r",

            encoding="utf-8"

        ) as file:


            return json.load(file)



    def get(
        self,
        section,
        key
    ):


        return self.config.get(

            section,

            {}

        ).get(

            key

        )



    def get_image_provider(
        self
    ):


        return self.config["providers"]["image"]["active"]