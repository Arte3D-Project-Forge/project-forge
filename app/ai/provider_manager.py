from app.ai.providers.mock_provider import MockProvider


class ProviderManager:

    def __init__(self):

        self.providers = {}

        self.active_provider = None

        self.load_default_providers()


    def load_default_providers(self):

        self.register_provider(
            MockProvider()
        )

        self.set_active_provider(
            "Mock Provider"
        )


    def register_provider(
        self,
        provider
    ):

        self.providers[
            provider.get_name()
        ] = provider


    def set_active_provider(
        self,
        provider_name
    ):

        if provider_name not in self.providers:

            raise ValueError(
                f"Provider '{provider_name}' não encontrado."
            )

        self.active_provider = self.providers[
            provider_name
        ]


    def get_provider(self):

        if self.active_provider is None:

            raise RuntimeError(
                "Nenhum provider ativo."
            )

        return self.active_provider


    def generate_text(
        self,
        prompt
    ):

        return self.get_provider().generate_text(
            prompt
        )


    def generate_json(
        self,
        prompt
    ):

        return self.get_provider().generate_json(
            prompt
        )


    def generate_image(
        self,
        prompt,
        output_path
    ):

        return self.get_provider().generate_image(
            prompt,
            output_path
        )


    def list_providers(self):

        return list(
            self.providers.keys()
        )