from abc import ABC, abstractmethod

import os
import json

from datetime import datetime



class ImageProvider(ABC):


    """
    Base interface for image generation providers.

    All image generators used by Project Forge
    must implement this contract.
    """



    def __init__(
        self,
        output_path="generated/images"
    ):


        self.output_path = output_path


        os.makedirs(

            self.output_path,

            exist_ok=True

        )



    @abstractmethod
    def generate(
        self,
        prompt,
        filename
    ):


        pass



    def save_metadata(
        self,
        filename,
        prompt,
        provider
    ):


        metadata = {


            "filename":

                filename,


            "provider":

                provider,


            "prompt":

                prompt,


            "created_at":

                datetime.now().isoformat()


        }



        metadata_path = os.path.join(

            self.output_path,

            filename + ".json"

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



        return metadata_path