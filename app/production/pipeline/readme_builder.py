import os
from datetime import datetime


class ReadmeBuilder:


    def __init__(self, job):

        self.job = job



    def build(self, package_path):

        filepath = os.path.join(
            package_path,
            "README.md"
        )


        content = []

        content.append(
            "# Project Forge Asset Package\n"
        )

        content.append(
            "## Job\n\n"
        )

        content.append(
            f"{self.job.job_id}\n\n"
        )


        content.append(
            "---\n\n"
        )


        content.append(
            "## Projeto\n\n"
        )

        content.append(
            f"{self.job.project['name']}\n\n"
        )

        content.append(
            "Engine:\n\n"
        )

        content.append(
            f"{self.job.project['engine']}\n\n"
        )


        content.append(
            "---\n\n"
        )


        content.append(
            "## Solicitação\n\n"
        )

        content.append(
            f"{self.job.request}\n\n"
        )


        content.append(
            "---\n\n"
        )


        content.append(
            "## Tarefas\n\n"
        )

        content.append(
            self.format_tasks()
        )

        content.append(
            "\n\n---\n\n"
        )


        content.append(
            "## Estrutura\n\n"
        )


        content.append(
            "concept/\n"
            "lore/\n"
            "sprites/\n"
            "animations/\n"
            "tiles/\n"
            "audio/\n"
            "ui/\n"
            "godot/\n"
            "metadata/\n"
            "prompts/\n\n"
        )


        content.append(
            "---\n\n"
        )


        content.append(
            "## Status\n\n"
        )

        content.append(
            f"Status: {self.job.status}\n"
        )

        content.append(
            f"Stage: {self.job.stage}\n"
        )

        content.append(
            f"Progress: {self.job.progress}%\n"
        )

        content.append(
            f"Priority: {self.job.priority}\n\n"
        )


        content.append(
            "## Gerado em\n\n"
        )

        content.append(
            datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )
        )


        content.append(
            "\n\nGerado automaticamente pelo Project Forge."
        )


        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "".join(content)
            )


        return filepath



    def format_tasks(self):

        return "\n".join(
            f"- {task}"
            for task in self.job.tasks
        )