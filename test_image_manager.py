from app.ai.manager.image_provider_manager import ImageProviderManager



manager = ImageProviderManager(

    provider_name="mock"

)



result = manager.generate(

    prompt="Ancient fire dragon pixel art RPG character 48x48",

    filename="ember_drake_idle_001"

)



print(result)