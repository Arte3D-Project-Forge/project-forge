from app.core.env_manager import EnvManager


env = EnvManager()

key = env.get("OPENAI_API_KEY")

if key:
    print("OPENAI KEY: OK (definida, nao exibida)")
else:
    print("OPENAI KEY: ausente")
