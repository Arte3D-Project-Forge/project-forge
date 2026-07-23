from app.database.asset_database import AssetDatabase



database = AssetDatabase()



asset = database.register_asset(

    asset_name="criar_um_dragão",

    asset_type="character",

    package_path="Forge_Test_02/generated/JOB-20260723-0001"

)



print(asset)



print()


print(
    "REGISTERED ASSETS:"
)


for item in database.get_assets():

    print(item)