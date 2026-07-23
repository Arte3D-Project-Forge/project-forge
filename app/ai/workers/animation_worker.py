import os
import json



class AnimationWorker:


    def __init__(
        self,
        provider_manager
    ):

        self.provider = provider_manager



    def run(
        self,
        job,
        package_path
    ):

        asset_name = self.create_asset_name(
            job.request
        )


        animation_path = os.path.join(

            package_path,

            "animations",

            asset_name

        )


        os.makedirs(

            animation_path,

            exist_ok=True

        )


        animations = self.get_animation_list()



        for animation in animations:


            data = self.create_animation_data(

                animation

            )


            filename = (

                animation

                +

                ".json"

            )


            filepath = os.path.join(

                animation_path,

                filename

            )


            with open(

                filepath,

                "w",

                encoding="utf-8"

            ) as file:


                json.dump(

                    data,

                    file,

                    indent=4,

                    ensure_ascii=False

                )



        metadata = self.create_metadata(

            asset_name,

            animations

        )


        metadata_file = os.path.join(

            animation_path,

            "animation_metadata.json"

        )


        with open(

            metadata_file,

            "w",

            encoding="utf-8"

        ) as file:


            json.dump(

                metadata,

                file,

                indent=4,

                ensure_ascii=False

            )


        return animation_path



    def create_asset_name(
        self,
        request
    ):

        words = request.lower().split()


        return "_".join(

            words[:3]

        )



    def get_animation_list(
        self
    ):


        return [

            "idle",

            "walk",

            "attack",

            "hurt",

            "death"

        ]



    def create_animation_data(
        self,
        animation
    ):


        configs = {


            "idle": {

                "frames": 4,

                "fps": 4,

                "loop": True,

                "direction": "horizontal"

            },


            "walk": {

                "frames": 6,

                "fps": 8,

                "loop": True,

                "direction": "horizontal"

            },


            "attack": {

                "frames": 6,

                "fps": 10,

                "loop": False,

                "direction": "horizontal"

            },


            "hurt": {

                "frames": 3,

                "fps": 8,

                "loop": False,

                "direction": "horizontal"

            },


            "death": {

                "frames": 8,

                "fps": 8,

                "loop": False,

                "direction": "horizontal"

            }

        }


        return {


            "animation": animation,


            **configs[animation],


            "status": "prepared"


        }



    def create_metadata(
        self,
        asset_name,
        animations
    ):


        return {


            "asset": asset_name,


            "type": "animation_set",


            "engine": "Godot",


            "animations": animations,


            "format": "AnimatedSprite2D Ready",


            "status": "prepared"


        }