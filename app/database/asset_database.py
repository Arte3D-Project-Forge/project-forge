import os
import json

from datetime import datetime

from app.utils.encoding import UTF8Normalizer
from app.database.versioning.version_manager import VersionManager



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


        self.version_manager = VersionManager(

            database_path

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


        display_name = UTF8Normalizer.fix(

            asset_name

        )


        internal_name = UTF8Normalizer.slug(

            display_name

        )


        asset_id = len(assets) + 1



        created = datetime.now().isoformat()



        asset = {


            "id":

                asset_id,


            "name":

                internal_name,


            "display_name":

                display_name,


            "type":

                asset_type,


            "path":

                package_path,


            "version":

                "1.0",


            "status":

                status,


            "created_at":

                created

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


        self.version_manager.create_version(

            asset_id,

            "1.0",

            [

                "initial asset creation",

                "production package generated",

                "quality approval completed"

            ]

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


                "display_name":

                    asset["display_name"],


                "type":

                    asset["type"],


                "status":

                    asset["status"]


            }

        )


        self.save(

            self.registry_file,

            registry

        )



    def get_assets(
        self
    ):


        return self.load(

            self.assets_file

        )