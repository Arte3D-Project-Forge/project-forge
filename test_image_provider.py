from app.ai.providers.images.mock_image_provider import MockImageProvider



provider = MockImageProvider()



result = provider.generate(

    prompt="Ancient fire dragon pixel art 48x48 RPG",

    filename="ember_drake_idle_001",

    output_path="test_output"

)



print(result)