from app.core.module import ForgeModule


class DocumentsModule(ForgeModule):


    def __init__(self):

        super().__init__(

            module_id="documents",

            name="Documents",

            category="Documentation",

            version="1.0",

            status="Stable"

        )


    def open(self):

        return (
            "Documents Module loaded successfully."
        )