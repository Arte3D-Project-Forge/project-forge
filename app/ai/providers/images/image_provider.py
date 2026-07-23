from abc import ABC, abstractmethod



class ImageProvider(ABC):


    """
    Base interface for Project Forge image providers.
    """


    @abstractmethod
    def generate(

        self,

        prompt,

        filename,

        output_path

    ):


        """
        Generate image asset.

        Args:

            prompt:
                Image generation prompt.

            filename:
                Asset filename.

            output_path:
                Final asset directory.

        Returns:

            Generation result dictionary.

        """


        pass