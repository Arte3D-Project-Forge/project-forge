import os
import json

from datetime import datetime

from app.ai.manager.image_provider_manager import ImageProviderManager



class SpriteWorker:


    def __init__(
        self,
        image_provider="mock"
    ):


        self.image_manager = ImageProviderManager(

            provider_name=image_provider

        )



    def generate(
        self,
        project,
        asset_name,
        prompt
    ):


        output_path = os.path.join(

            project["path"],

            "sprites",

            asset_name

        )


        animations = [

            "idle",

            "walk",

            "attack",

            "hurt",

            "death"

        ]



        os.makedirs(

            output_path,

            exist_ok=True

        )



        generated_files = []



        for animation in animations:


            animation_path = os.path.join(

                output_path,

                animation

            )


            os.makedirs(

                animation_path,

                exist_ok=True

            )


            filename = (

                asset_name

                +

                "_"

                +

                animation

                +

                "_001"

            )



            result = self.image_manager.generate(

                prompt=(

                    prompt

                    +

                    f" animation {animation}"

                ),

                filename=filename

            )


            generated_files.append(

                result

            )



        metadata = {


            "asset":

                asset_name,


            "type":

                "sprite",


            "animations":

                animations,


            "generated_files":

                generated_files,


            "created_at":

                datetime.now().isoformat()

        }



        metadata_path = os.path.join(

            output_path,

            "sprite_generation.json"

        )



        with open(

            metadata_path,

            "w",

            encoding="utf-8"

        ) as file:


            json.dump(

                metadata,

                file,

                indent=4,

                ensure_ascii=False

            )



        return output_path