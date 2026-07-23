import json
import os
from datetime import datetime


class ManifestBuilder:

    def __init__(self, job):

        self.job = job


    def build(self, package_path):

        manifest = {

            "job_id": self.job.job_id,

            "project": self.job.project["name"],

            "engine": self.job.project["engine"],

            "request": self.job.request,

            "tasks": self.job.tasks,

            "status": self.job.status,

            "stage": self.job.stage,

            "priority": self.job.priority,

            "progress": self.job.progress,

            "created_at": self.job.created_at.isoformat(),

            "generated_at": datetime.now().isoformat(),

            "generator": "Project Forge",

            "version": "1.0"

        }

        filepath = os.path.join(
            package_path,
            "manifest.json"
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                manifest,
                file,
                indent=4,
                ensure_ascii=False
            )

        return filepath