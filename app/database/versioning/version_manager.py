import os
import json

from datetime import datetime



class VersionManager:


    def __init__(
        self,
        database_path="database"
    ):


        self.database_path = database_path


        os.makedirs(

            self.database_path,

            exist_ok=True

        )


        self.changelog_file = os.path.join(

            self.database_path,

            "changelog.json"

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

            self.changelog_file,

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



    def create_version(
        self,
        asset_id,
        version,
        changes
    ):


        versions = self.load(

            self.versions_file

        )


        version_data = {


            "asset_id":

                asset_id,


            "version":

                version,


            "changes":

                changes,


            "created_at":

                datetime.now().isoformat()

        }



        versions.append(

            version_data

        )


        self.save(

            self.versions_file,

            versions

        )


        self.create_changelog(

            version_data

        )


        return version_data



    def create_changelog(
        self,
        version_data
    ):


        changelog = self.load(

            self.changelog_file

        )


        changelog.append(

            {


                "asset_id":

                    version_data["asset_id"],


                "version":

                    version_data["version"],


                "summary":

                    ", ".join(

                        version_data["changes"]

                    ),


                "date":

                    version_data["created_at"]


            }

        )


        self.save(

            self.changelog_file,

            changelog

        )



    def get_versions(
        self,
        asset_id=None
    ):


        versions = self.load(

            self.versions_file

        )


        if asset_id is None:


            return versions



        return [

            version

            for version in versions

            if version["asset_id"] == asset_id

        ]