import os
import json


class SpriteWorker:


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


        sprite_path = os.path.join(

            package_path,

            "sprites",

            asset_name

        )


        self.create_structure(
            sprite_path
        )


        metadata = self.create_metadata(
            job,
            asset_name
        )


        metadata_file = os.path.join(

            sprite_path,

            "metadata.json"

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



        prompt = self.build_prompt(
            job,
            asset_name
        )


        prompt_file = os.path.join(

            sprite_path,

            "sprite_prompt.txt"

        )


        with open(

            prompt_file,

            "w",

            encoding="utf-8"

        ) as file:

            file.write(
                prompt
            )



        return sprite_path



    def create_structure(
        self,
        path
    ):

        animations = [

            "idle",

            "walk",

            "attack",

            "hurt",

            "death"

        ]


        for animation in animations:

            os.makedirs(

                os.path.join(

                    path,

                    animation

                ),

                exist_ok=True

            )



    def create_asset_name(
        self,
        request
    ):

        words = request.lower().split()

        name = "_".join(
            words[:3]
        )

        return name



    def create_metadata(
        self,
        job,
        asset_name
    ):

        return {

            "asset": asset_name,

            "type": "character_sprite",

            "style": "HD Pixel Art",

            "resolution": "48x48",

            "engine": job.project["engine"],

            "animations": [

                "idle",

                "walk",

                "attack",

                "hurt",

                "death"

            ],

            "status": "prepared"

        }



    def build_prompt(
        self,
        job,
        asset_name
    ):

        return f"""
Create a professional RPG pixel art sprite.

Asset:
{asset_name}

Description:
{job.request}

Style:
HD Pixel Art

Resolution:
48x48 pixels

Requirements:

- Transparent background
- Game ready sprite
- RPG fantasy style
- Consistent animation frames
- Idle animation
- Walk animation
- Attack animation
- Hurt animation
- Death animation

Engine:
{job.project["engine"]}
""".strip()