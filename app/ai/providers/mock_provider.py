import json
import os

from app.ai.providers.base_provider import BaseProvider


class MockProvider(BaseProvider):

    def get_name(self):

        return "Mock Provider"


    def generate_text(self, prompt):

        return (
            "========== MOCK RESPONSE ==========\n\n"
            + prompt +
            "\n\n=================================="
        )


    def generate_json(self, prompt):

        return {

            "provider": "mock",

            "success": True,

            "prompt": prompt

        }


    def generate_image(

        self,

        prompt,

        output_path

    ):

        os.makedirs(

            os.path.dirname(output_path),

            exist_ok=True

        )


        data = {

            "provider": "mock",

            "image": "not_generated",

            "prompt": prompt

        }


        fake_image = (

            output_path +

            ".json"

        )


        with open(

            fake_image,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                data,

                file,

                indent=4,

                ensure_ascii=False

            )


        return fake_image