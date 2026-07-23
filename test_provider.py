from app.ai.provider_manager import ProviderManager


manager = ProviderManager()

print()

print("Provider ativo:")

print(manager.get_provider().get_name())

print()

print("Lista de providers:")

print(manager.list_providers())

print()

print("Teste texto:")

print(

    manager.generate_text(

        "Criar um dragão de fogo."

    )

)

print()

print("Teste JSON:")

print(

    manager.generate_json(

        "Criar um dragão de fogo."

    )

)

print()

print("Teste imagem:")

path = manager.generate_image(

    "Criar um dragão.",

    "teste/dragon.png"

)

print(path)

print()

print("Fim.")