import os


class PackageBuilder:

    def __init__(self, job):

        self.job = job


    def build(self):

        project_path = self.job.project["path"]

        output_path = os.path.join(
            project_path,
            "generated",
            self.job.job_id
        )

        folders = [

            "prompts",

            "lore",

            "concept",

            "sprites",

            "animations",

            "tiles",

            "audio",

            "ui",

            "godot",

            "metadata"

        ]

        os.makedirs(
            output_path,
            exist_ok=True
        )

        for folder in folders:

            os.makedirs(
                os.path.join(
                    output_path,
                    folder
                ),
                exist_ok=True
            )

        return output_path