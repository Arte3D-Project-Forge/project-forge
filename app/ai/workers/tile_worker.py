import os
import json


class TileWorker:


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

        biome_name = self.create_biome_name(
            job.request
        )


        tile_path = os.path.join(

            package_path,

            "tiles",

            biome_name

        )


        self.create_structure(
            tile_path
        )


        metadata = self.create_metadata(
            job,
            biome_name
        )


        metadata_file = os.path.join(

            tile_path,

            "tile_metadata.json"

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
            biome_name
        )


        prompt_file = os.path.join(

            tile_path,

            "tile_prompt.txt"

        )


        with open(

            prompt_file,

            "w",

            encoding="utf-8"

        ) as file:


            file.write(
                prompt
            )


        return tile_path



    def create_structure(
        self,
        path
    ):


        folders = [

            "terrain",

            "vegetation",

            "water",

            "props"

        ]


        for folder in folders:


            os.makedirs(

                os.path.join(

                    path,

                    folder

                ),

                exist_ok=True

            )



    def create_biome_name(
        self,
        request
    ):


        words = request.lower().split()


        name = "_".join(

            words[:2]

        )


        return name



    def create_metadata(
        self,
        job,
        biome_name
    ):


        return {


            "biome": biome_name,


            "type": "environment_tiles",


            "style": "HD Pixel Art",


            "tile_size": "32x32",


            "engine": job.project["engine"],


            "categories": [

                "terrain",

                "vegetation",

                "water",

                "props"

            ],


            "status": "prepared"


        }



    def build_prompt(
        self,
        job,
        biome_name
    ):


        return f"""
Create a professional RPG environment tile set.

Biome:
{biome_name}

Description:
{job.request}

Style:
HD Pixel Art

Tile Size:
32x32 pixels

Requirements:

- Seamless tiles
- RPG fantasy environment
- Godot compatible
- Terrain variations
- Vegetation assets
- Water tiles
- Environmental props
- Consistent art direction

Engine:
{job.project["engine"]}
""".strip()