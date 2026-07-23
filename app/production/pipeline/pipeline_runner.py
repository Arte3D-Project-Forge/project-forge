from app.production.pipeline.package_builder import PackageBuilder
from app.production.pipeline.manifest_builder import ManifestBuilder
from app.production.pipeline.prompt_builder import PromptBuilder
from app.production.pipeline.readme_builder import ReadmeBuilder

from app.ai.provider_manager import ProviderManager
from app.ai.workers.lore_worker import LoreWorker



class PipelineRunner:


    def __init__(
        self,
        job
    ):

        self.job = job


        self.package = PackageBuilder(
            job
        )


        self.manifest = ManifestBuilder(
            job
        )


        self.prompts = PromptBuilder(
            job
        )


        self.readme = ReadmeBuilder(
            job
        )


        self.provider = ProviderManager()


        self.lore_worker = LoreWorker(
            self.provider
        )



    def run(self):

        print(
            "========== PROJECT FORGE =========="
        )

        print(
            "Starting Production Pipeline..."
        )


        print()


        package_path = self.package.build()


        print(
            "[OK] Package created"
        )


        self.manifest.build(
            package_path
        )


        print(
            "[OK] Manifest generated"
        )



        self.prompts.build(
            package_path
        )


        print(
            "[OK] Prompts generated"
        )



        self.readme.build(
            package_path
        )


        print(
            "[OK] README generated"
        )



        lore_file = self.lore_worker.run(

            self.job,

            package_path

        )


        print(
            "[OK] Lore generated"
        )


        print(
            lore_file
        )


        print()

        print(
            "Production completed."
        )


        return package_path