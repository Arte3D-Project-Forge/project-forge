import os
import json
from datetime import datetime



class AssetDatabase:


    def __init__(
        self,
        database_path="database"
    ):


        self.database_path = database_path


        os.makedirs(

            self.database_path,

            exist_ok=True

        )


        self.assets_file = os.path.join(

            self.database_path,

            "assets.json"

        )


        self.registry_file = os.path.join(

            self.database_path,

            "registry.json"

        )


        self.versions_file = os.path.join(

            self.database_path,

            "versions.json"

        )


        self.initialize()



    def initialize(
        self
    ):


        files = [

            self.assets_file,

            self.registry_file,

            self.versions_file

        ]


        for file in files:


            if not os.path.exists(file):


                with open(

                    file,

                    "w",

                    encoding="utf-8"

                ) as f:


                    json.dump(

                        [],

                        f,

                        indent=4,

                        ensure_ascii=False

                    )



    def load(
        self,
        file
    ):


        with open(

            file,

            "r",

            encoding="utf-8"

        ) as f:


            return json.load(f)



    def save(
        self,
        file,
        data
    ):


        with open(

            file,

            "w",

            encoding="utf-8"

        ) as f:


            json.dump(

                data,

                f,

                indent=4,

                ensure_ascii=False

            )



    def register_asset(
        self,
        asset_name,
        asset_type,
        package_path,
        status="approved"
    ):


        assets = self.load(

            self.assets_file

        )


        asset = {


            "id":

                len(assets) + 1,


            "name":

                asset_name,


            "type":

                asset_type,


            "path":

                package_path,


            "version":

                "1.0",


            "status":

                status,


            "created_at":

                datetime.now().isoformat()

        }



        assets.append(

            asset

        )


        self.save(

            self.assets_file,

            assets

        )


        self.update_registry(

            asset

        )


        self.create_version(

            asset

        )


        return asset



    def update_registry(
        self,
        asset
    ):


        registry = self.load(

            self.registry_file

        )


        registry.append(

            {

                "asset_id":

                    asset["id"],


                "name":

                    asset["name"],


                "type":

                    asset["type"]

            }

        )


        self.save(

            self.registry_file,

            registry

        )



    def create_version(
        self,
        asset
    ):


        versions = self.load(

            self.versions_file

        )


        versions.append(

            {

                "asset_id":

                    asset["id"],


                "version":

                    asset["version"],


                "date":

                    asset["created_at"]

            }

        )


        self.save(

            self.versions_file,

            versions

        )



    def get_assets(
        self
    ):


        return self.load(

            self.assets_file

        )