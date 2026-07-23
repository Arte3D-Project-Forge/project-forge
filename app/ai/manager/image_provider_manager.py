from app.core.config_manager import ConfigManager

from app.ai.providers.images.mock_image_provider import MockImageProvider



class ImageProviderManager:


    def __init__(

        self

    ):


        self.config = ConfigManager()


        self.provider_name = (

            self.config.get_image_provider()

        )


        self.provider = self.load_provider()



    def load_provider(

        self

    ):


        if self.provider_name == "mock":


            return MockImageProvider()



        raise Exception(

            f"Unsupported image provider: {self.provider_name}"

        )



    def generate(

        self,

        prompt,

        filename

    ):


        return self.provider.generate(

            prompt,

            filename

        )