from abc import ABC, abstractmethod



class ImageProvider(ABC):


    """
    Base interface for all Project Forge image providers.
    Every image provider must implement generate().
    """



    @abstractmethod
    def generate(

        self,

        prompt,

        filename

    ):


        """
        Generate an image asset.

        Args:
            prompt:
                Description used by the image model.

            filename:
                Target asset name.

        Returns:
            Provider generation result.
        """


        pass