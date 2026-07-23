from app.ai.workers.sprite_worker import SpriteWorker



project = {


    "path":

        "Forge_Test_03/generated"


}



worker = SpriteWorker()



result = worker.generate(

    project,

    "ember_drake",

    "Ancient fire dragon HD pixel art RPG character 48x48"

)



print(result)