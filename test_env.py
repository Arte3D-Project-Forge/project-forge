from app.core.env_manager import EnvManager



env = EnvManager()



print(

    "OPENAI KEY:",

    env.get(

        "OPENAI_API_KEY"

    )

)