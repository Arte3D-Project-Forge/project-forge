import os



class AssetQualityManager:


    def __init__(self):

        self.results = []



    def validate(
        self,
        package_path
    ):


        self.results = []


        self.check_folder(

            package_path,

            "sprites",

            "Sprites"

        )


        self.check_folder(

            package_path,

            "tiles",

            "Tiles"

        )


        self.check_folder(

            package_path,

            "animations",

            "Animations"

        )


        self.check_folder(

            package_path,

            "audio",

            "Audio"

        )


        self.check_folder(

            package_path,

            "godot",

            "Godot"

        )



        return self.build_report()



    def check_folder(
        self,
        package_path,
        folder,
        name
    ):


        path = os.path.join(

            package_path,

            folder

        )


        exists = os.path.exists(

            path

        )


        self.results.append(

            {

                "name": name,

                "status":

                    "OK"

                    if exists

                    else

                    "FAILED"

            }

        )



    def build_report(
        self
    ):


        approved = all(

            item["status"] == "OK"

            for item in self.results

        )


        return {


            "status":

                "APPROVED"

                if approved

                else

                "FAILED",


            "checks":

                self.results

        }



    def print_report(
        self,
        report
    ):


        print()

        print(
            "========== QUALITY CHECK =========="
        )


        for item in report["checks"]:


            print(

                f'{item["name"]}: '

                f'{item["status"]}'

            )


        print()


        print(

            "PACKAGE STATUS: "

            +

            report["status"]

        )