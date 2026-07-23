from app.database.versioning.version_manager import VersionManager



manager = VersionManager()



version = manager.create_version(

    asset_id=1,

    version="1.1",

    changes=[

        "new attack animation",

        "improved sprite",

        "updated godot scene"

    ]

)



print(version)



print()



print(
    "VERSION HISTORY:"
)



for item in manager.get_versions(1):

    print(item)