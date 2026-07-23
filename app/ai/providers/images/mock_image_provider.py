import json
import os

from datetime import datetime

from app.ai.providers.images.image_provider import ImageProvider



class MockImageProvider(ImageProvider):


    def generate(

        self,

        prompt,

        filename

    ):


        output_path = os.path.join(

            "generated",

            "images"

        )


        os.makedirs(

            output_path,

            exist_ok=True

        )


        file_path = os.path.join(

            output_path,

            filename + ".json"

        )


        data = {


            "status":

                "generated",


            "provider":

                "mock",


            "filename":

                filename,


            "prompt":

                prompt,


            "created_at":

                datetime.now().isoformat()

        }



        with open(

            file_path,

            "w",

            encoding="utf-8"

        ) as file:


            json.dump(

                data,

                file,

                indent=4,

                ensure_ascii=False

            )



        return data