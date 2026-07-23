import os


class LoreWorker:

    def __init__(
        self,
        provider_manager
    ):

        self.provider = provider_manager


    def run(
        self,
        job,
        package_path
    ):

        prompt = self.build_prompt(
            job
        )


        response = self.provider.generate_text(
            prompt
        )


        lore_path = os.path.join(

            package_path,

            "lore",

            "generated_lore.md"

        )


        os.makedirs(

            os.path.dirname(lore_path),

            exist_ok=True

        )


        content = self.format_lore(
            job,
            response
        )


        with open(

            lore_path,

            "w",

            encoding="utf-8"

        ) as file:

            file.write(
                content
            )


        return lore_path



    def build_prompt(
        self,
        job
    ):

        return f"""
Você é um Game Writer profissional especializado em RPG.

Projeto:

{job.project["name"]}


Pedido:

{job.request}


Crie:

- Nome do personagem ou criatura
- História
- Origem
- Habitat
- Aparência
- Habilidades
- Fraquezas
- Personalidade
- Raridade
- Elemento
- Classificação no mundo do jogo


Escreva como um documento oficial de Game Design.
""".strip()



    def format_lore(
        self,
        job,
        response
    ):

        return f"""
# Lore Generated

## Projeto

{job.project["name"]}


## Solicitação

{job.request}


---

## Conteúdo

{response}


---

Gerado pelo Project Forge.
""".strip()