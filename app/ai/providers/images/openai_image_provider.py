import os
import base64

from datetime import datetime

from openai import OpenAI

from app.ai.providers.images.image_provider import ImageProvider
from app.core.env_manager import EnvManager


class OpenAIImageProvider(ImageProvider):

    def __init__(self):

        self.env = EnvManager()

        self.api_key = self.env.get("OPENAI_API_KEY")

        if not self.api_key:
            raise Exception(
                "OPENAI_API_KEY not configured in config/.env"
            )

        self.client = OpenAI(
            api_key=self.api_key
        )

    def generate(
        self,
        prompt,
        filename,
        output_path
    ):

        try:

            os.makedirs(
                output_path,
                exist_ok=True
            )

            response = self.client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size="1024x1024",
                quality="medium",
                background="transparent"
            )

            if (
                not response.data
                or not response.data[0].b64_json
            ):
                raise Exception(
                    "OpenAI returned no image."
                )

            image_bytes = base64.b64decode(
                response.data[0].b64_json
            )

            file_path = os.path.join(
                output_path,
                filename + ".png"
            )

            with open(
                file_path,
                "wb"
            ) as image_file:

                image_file.write(
                    image_bytes
                )

            return {

                "status": "generated",

                "provider": "openai",

                "file": file_path,

                "created_at": datetime.now().isoformat()

            }

        except Exception as error:

            return {

                "status": "error",

                "provider": "openai",

                "message": str(error)

            }