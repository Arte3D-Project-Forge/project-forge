import unicodedata



class UTF8Normalizer:


    @staticmethod
    def fix(
        text
    ):


        if not isinstance(
            text,
            str
        ):

            return text



        replacements = {


            "Ã¡": "á",
            "Ã ": "à",
            "Ã£": "ã",
            "Ã¢": "â",
            "Ã¤": "ä",

            "Ã©": "é",
            "Ã¨": "è",
            "Ãª": "ê",

            "Ã­": "í",
            "Ã³": "ó",
            "Ãµ": "õ",
            "Ã´": "ô",

            "Ãº": "ú",
            "Ã§": "ç",

            "Â": ""

        }



        for wrong, correct in replacements.items():


            text = text.replace(

                wrong,

                correct

            )



        return unicodedata.normalize(

            "NFC",

            text

        )



    @staticmethod
    def slug(
        text
    ):


        text = UTF8Normalizer.fix(

            text

        )


        replacements = {


            "á":"a",
            "à":"a",
            "ã":"a",
            "â":"a",
            "ä":"a",

            "é":"e",
            "è":"e",
            "ê":"e",

            "í":"i",

            "ó":"o",
            "ò":"o",
            "õ":"o",
            "ô":"o",

            "ú":"u",

            "ç":"c"

        }



        result = text.lower()



        for old,new in replacements.items():

            result = result.replace(

                old,

                new

            )



        result = result.replace(

            " ",

            "_"

        )


        result = result.replace(

            "-",

            "_"

        )


        allowed = (

            "abcdefghijklmnopqrstuvwxyz"

            "0123456789_"

        )


        return "".join(

            char

            for char in result

            if char in allowed

        )