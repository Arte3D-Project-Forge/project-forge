import json
import os


class ProjectManager:

    def __init__(self):

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        )

        self.file = os.path.join(
            base_dir,
            "app",
            "data",
            "projects.json"
        )


    def load_projects(self):

        if not os.path.exists(self.file):

            return []


        with open(
            self.file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def save_project(self, project):

        projects = self.load_projects()


        data = {

            "name": project.name,

            "engine": project.engine,

            "path": os.path.abspath(
                project.name.replace(" ", "_")
            )
        }


        projects.append(data)


        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                projects,
                f,
                indent=4,
                ensure_ascii=False
            )