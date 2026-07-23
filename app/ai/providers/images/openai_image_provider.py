import os
import base64

from datetime import datetime

from app.ai.providers.images.image_provider import ImageProvider



class OpenAIImageProvider(ImageProvider):


    def __init__(

        self

    ):


        self.api_key = os.getenv(

            "OPENAI_API_KEY"

        )


        if not self.api_key:

            raise Exception(

                "OPENAI_API_KEY not configured"

            )



    def generate(

        self,

        prompt,

        filename

    ):


        """
        OpenAI image generation provider.

        This implementation prepares the
        generation pipeline and API connection.

        """


        try:


            from openai import OpenAI



            client = OpenAI(

                api_key=self.api_key

            )



            response = client.images.generate(

                model="gpt-image-1",

                prompt=prompt,

                size="1024x1024",

                quality="medium"

            )



            image_data = response.data[0].b64_json



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

                filename + ".png"

            )



            with open(

                file_path,

                "wb"

            ) as file:


                file.write(

                    base64.b64decode(

                        image_data

                    )

                )



            return {


                "status":

                    "generated",


                "provider":

                    "openai",


                "file":

                    file_path,


                "created_at":

                    datetime.now().isoformat()

            }



        except Exception as error:


            return {


                "status":

                    "error",


                "provider":

                    "openai",


                "message":

                    str(error)

            }