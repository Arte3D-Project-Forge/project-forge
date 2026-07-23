import os


class PromptBuilder:

    def __init__(self, job):

        self.job = job


    def build(self, package_path):

        prompts_path = os.path.join(
            package_path,
            "prompts"
        )

        os.makedirs(
            prompts_path,
            exist_ok=True
        )

        prompt_files = {

            "lore.txt": self.build_lore_prompt(),

            "sprites.txt": self.build_sprite_prompt(),

            "animations.txt": self.build_animation_prompt(),

            "tiles.txt": self.build_tiles_prompt(),

            "godot.txt": self.build_godot_prompt()

        }

        for filename, content in prompt_files.items():

            filepath = os.path.join(
                prompts_path,
                filename
            )

            with open(
                filepath,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(content)

        return prompts_path


    def build_lore_prompt(self):

        return f"""
Você é um Game Designer profissional.

Projeto:
{self.job.project["name"]}

Engine:
{self.job.project["engine"]}

Pedido:
{self.job.request}

Crie uma lore completa.

Inclua:

- História
- Origem
- Habitat
- Personalidade
- Habilidades
- Fraquezas
- Curiosidades
""".strip()


    def build_sprite_prompt(self):

        return f"""
Você é um Pixel Artist profissional.

Pedido:

{self.job.request}

Produza sprites prontos para Godot.

Requisitos:

- Pixel Art

- Fundo transparente

- Vista Top Down

- Estilo Zelda

- Consistência visual

- Sprite Sheet organizada
""".strip()


    def build_animation_prompt(self):

        return f"""
Crie animações para:

{self.job.request}

Gerar:

Idle

Walk

Attack

Hit

Death

Separadas em Sprite Sheets.
""".strip()


    def build_tiles_prompt(self):

        return f"""
Crie Tiles compatíveis com:

{self.job.request}

Produzir:

Floor

Grass

Stone

Decoration

Collision

Autotile

Godot Ready.
""".strip()


    def build_godot_prompt(self):

        return f"""
Preparar assets para Godot.

Projeto:

{self.job.project["name"]}

Organizar:

Sprites

Animations

Textures

Import Settings

Nomenclatura consistente.

Pronto para uso imediato.
""".strip()