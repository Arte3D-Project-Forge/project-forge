import os



class EnvManager:


    def __init__(

        self,

        env_path="config/.env"

    ):


        self.env_path = env_path

        self.load()



    def load(

        self

    ):


        if not os.path.exists(

            self.env_path

        ):

            return



        with open(

            self.env_path,

            "r",

            encoding="utf-8"

        ) as file:


            for line in file:


                line = line.strip()



                if not line:

                    continue



                if line.startswith("#"):

                    continue



                key, value = line.split(

                    "=",

                    1

                )


                os.environ[key] = value



    def get(

        self,

        key

    ):


        return os.getenv(

            key

        )