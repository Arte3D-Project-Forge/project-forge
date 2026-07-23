from app.production.production_job import ProductionJob
from app.production.pipeline.pipeline_runner import PipelineRunner



project = {

    "name": "Forge_Test_02",

    "engine": "Godot",

    "path": "Forge_Test_02"

}



job = ProductionJob(

    project,

    "Criar um dragão de fogo ancestral pixel art para RPG",

    [

        "lore",

        "sprites",

        "animation",

        "tiles"

    ]

)



job.save()



pipeline = PipelineRunner(

    job

)



result = pipeline.run()



print()

print(
    "OUTPUT:"
)

print(
    result
)