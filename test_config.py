from app.core.config_manager import ConfigManager



config = ConfigManager()



print(

    "Image Provider:",

    config.get_image_provider()

)


print(

    "Resolution:",

    config.get(

        "generation",

        "default_resolution"

    )

)