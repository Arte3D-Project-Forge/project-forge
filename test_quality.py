from app.quality.asset_quality_manager import AssetQualityManager



package = (

    "Forge_Test_02/generated/"

    "JOB-20260723-0001"

)



manager = AssetQualityManager()


report = manager.validate(

    package

)


manager.print_report(

    report

)