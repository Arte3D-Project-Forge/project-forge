from app.ai.providers.images.image_provider import ImageProvider



class MockImageProvider(
    ImageProvider
):


    def generate(
        self,
        prompt,
        filename
    ):


        self.save_metadata(

            filename,

            prompt,

            "mock"

        )


        return {

            "status": "generated",

            "file":

                filename,

            "provider":

                "mock"

        }