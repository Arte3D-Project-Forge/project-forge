import os
import json



class AudioWorker:


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


        audio_path = os.path.join(

            package_path,

            "audio",

            asset_name

        )


        self.create_structure(
            audio_path
        )


        tracks = self.get_audio_tracks()



        for track in tracks:


            data = self.create_audio_data(

                track

            )


            filename = (

                track

                +

                ".json"

            )


            filepath = os.path.join(

                audio_path,

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

            tracks

        )


        metadata_file = os.path.join(

            audio_path,

            "audio_metadata.json"

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



        return audio_path



    def create_structure(
        self,
        path
    ):


        folders = [

            "music",

            "sfx",

            "ambient"

        ]


        for folder in folders:


            os.makedirs(

                os.path.join(

                    path,

                    folder

                ),

                exist_ok=True

            )



    def create_asset_name(
        self,
        request
    ):


        words = request.lower().split()


        return "_".join(

            words[:3]

        )



    def get_audio_tracks(
        self
    ):


        return [

            "main_theme",

            "biome_theme",

            "battle_theme",

            "attack_sfx",

            "hurt_sfx",

            "death_sfx",

            "environment_ambient"

        ]



    def create_audio_data(
        self,
        track
    ):


        categories = {


            "main_theme": "music",

            "biome_theme": "music",

            "battle_theme": "music",

            "attack_sfx": "sfx",

            "hurt_sfx": "sfx",

            "death_sfx": "sfx",

            "environment_ambient": "ambient"

        }



        return {


            "track": track,


            "category": categories[track],


            "style": "Fantasy RPG",


            "format": "game_ready_audio",


            "loop":

                track not in [

                    "attack_sfx",

                    "hurt_sfx",

                    "death_sfx"

                ],


            "status": "prepared"


        }



    def create_metadata(
        self,
        asset_name,
        tracks
    ):


        return {


            "asset": asset_name,


            "type": "audio_package",


            "tracks": tracks,


            "style": "Fantasy RPG",


            "engine": "Godot",


            "status": "prepared"


        }