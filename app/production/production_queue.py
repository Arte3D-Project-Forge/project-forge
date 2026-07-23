import os
import json


class ProductionQueue:


    def __init__(self, project):

        self.project = project

        self.jobs_path = os.path.join(
            project["path"],
            "jobs"
        )


    def get_jobs(self):

        if not os.path.exists(
            self.jobs_path
        ):

            return []


        jobs = []


        for file in os.listdir(
            self.jobs_path
        ):

            if file.endswith(".json"):

                path = os.path.join(
                    self.jobs_path,
                    file
                )


                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    jobs.append(
                        json.load(f)
                    )


        return jobs



    def count(self):

        return len(
            self.get_jobs()
        )



    def clear_completed(self):

        removed = 0


        for job in self.get_jobs():

            if job.get(
                "status"
            ) == "completed":

                removed += 1


        return removed