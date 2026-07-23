from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def generate_text(self, prompt):
        pass


    @abstractmethod
    def generate_image(self, prompt, output_path):
        pass


    @abstractmethod
    def generate_json(self, prompt):
        pass


    @abstractmethod
    def get_name(self):
        pass