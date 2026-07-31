import json
import os
import sys



class ConfigManager:


    def __init__(
        self,
        config_path="config/forge_config.json"
    ):

        self.config_path = self._resolve_path(
            config_path
        )

        self.config = self.load()



    def _resolve_path(self, path):

        if getattr(sys, "frozen", False):
            return self._resolve_frozen_path(path)

        if os.path.exists(path):
            return path

        base = getattr(
            sys, "_MEIPASS",
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )

        resolved = os.path.join(base, path)

        if os.path.exists(resolved):
            return resolved

        return path

    def _resolve_frozen_path(self, path):
        import shutil

        appdata = os.environ.get(
            "APPDATA",
            os.path.expanduser("~")
        )
        forge_dir = os.path.join(
            appdata, "ProjectForge"
        )

        writable = os.path.join(forge_dir, path)

        if os.path.exists(writable):
            return writable

        bundled = os.path.join(
            getattr(sys, "_MEIPASS", ""),
            path
        )

        os.makedirs(
            os.path.dirname(writable),
            exist_ok=True
        )

        if os.path.exists(bundled):
            shutil.copy(bundled, writable)

        return writable



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


    def set(
        self,
        section,
        key,
        value
    ):

        if section not in self.config:
            self.config[section] = {}

        self.config[section][key] = value

        with open(
            self.config_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self.config,
                file,
                indent=4,
                ensure_ascii=False
            )