from app.utils.encoding import UTF8Normalizer



tests = [

    "dragÃ£o",

    "dragão",

    "Criatura Mágica",

    "Espada Épica"

]



for item in tests:


    print(

        "Original:",

        item

    )


    print(

        "Fixado:",

        UTF8Normalizer.fix(item)

    )


    print(

        "Slug:",

        UTF8Normalizer.slug(item)

    )


    print(
        "----------------"
    )