import os


from app.ai.providers.images.mock_image_provider import MockImageProvider



class ImageProviderManager:


    def __init__(
        self,
        provider_name="mock"
    ):


        self.provider_name = provider_name


        self.provider = self.load_provider()



    def load_provider(
        self
    ):


        if self.provider_name == "mock":


            return MockImageProvider()



        raise Exception(

            f"Image provider not found: {self.provider_name}"

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