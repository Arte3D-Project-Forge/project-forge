import os


class ProjectCreator:

    def create(self, project):

        folder = project.name.replace(" ", "_")

        structure = [
            "",
            "assets",
            "assets/characters",
            "assets/environment",
            "assets/audio",
            "assets/ui",
            "docs",
            "src",
            "tools"
        ]

        os.makedirs(folder, exist_ok=True)

        for path in structure:
            os.makedirs(
                os.path.join(folder, path),
                exist_ok=True
            )

        self.create_files(folder, project)


    def create_files(self, folder, project):

        files = {

            "README.md":
            f"# {project.name}\n\nEngine: {project.engine}",

            "AGENTS.md":
            "Project Forge AI Agent Configuration",

            ".gitignore":
            "__pycache__/\n*.pyc",

            "docs/GAME_DESIGN.md":
            "# Game Design Document",

            "docs/LORE.md":
            "# Lore",

            "docs/ROADMAP.md":
            "# Roadmap"
        }


        for file, content in files.items():

            path = os.path.join(folder, file)

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(content)