import json
import os

from datetime import datetime


class ProductionJob:


    counter = 1


    def __init__(
        self,
        project,
        request,
        tasks
    ):

        self.project = project

        self.request = request

        self.tasks = tasks


        self.job_id = (

            f"JOB-"
            f"{datetime.now().strftime('%Y%m%d')}-"
            f"{ProductionJob.counter:04d}"

        )


        ProductionJob.counter += 1


        self.status = "queued"

        self.stage = "waiting"

        self.progress = 0

        self.priority = "normal"


        self.created_at = datetime.now()



    def build_data(self):


        return {


            "job_id": self.job_id,


            "project": self.project["name"],


            "engine": self.project["engine"],


            "request": self.request,


            "tasks": self.tasks,


            "status": self.status,


            "stage": self.stage,


            "progress": self.progress,


            "priority": self.priority,


            "created_at":
                self.created_at.isoformat()

        }



    def save(self):


        jobs_path = os.path.join(

            self.project["path"],

            "jobs"

        )


        os.makedirs(

            jobs_path,

            exist_ok=True

        )



        filename = (

            self.job_id

            +

            ".json"

        )



        filepath = os.path.join(

            jobs_path,

            filename

        )



        with open(

            filepath,

            "w",

            encoding="utf-8"

        ) as f:


            json.dump(

                self.build_data(),

                f,

                indent=4,

                ensure_ascii=False

            )



        return filepath