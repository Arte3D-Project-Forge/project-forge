from app.ai.workers.sprite_worker import SpriteWorker


class ProductionRunner:

    def __init__(self):

        self.sprite_worker = SpriteWorker()


    def run(self, job):

        print(f"Iniciando {job.job_id}")

        if "sprites" in job.tasks:

            self.run_sprites(job)

        print("Produção concluída.")


    def run_sprites(self, job):

        self.sprite_worker.generate(

            project=job.project,

            asset_name="generated_asset",

            prompt=job.request

        )