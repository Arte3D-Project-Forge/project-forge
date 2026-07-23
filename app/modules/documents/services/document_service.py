import os



class DocumentService:


    def __init__(self, project_path):

        self.project_path = project_path

        self.documents_path = os.path.join(
            project_path,
            "docs"
        )


        self.ensure_directory()



    def ensure_directory(self):

        if not os.path.exists(
            self.documents_path
        ):

            os.makedirs(
                self.documents_path
            )



    def list_documents(self):

        return os.listdir(
            self.documents_path
        )



    def create_document(
        self,
        name,
        content=""
    ):


        filename = (
            name
            if name.endswith(".md")
            else name + ".md"
        )


        path = os.path.join(
            self.documents_path,
            filename
        )


        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                content
            )


        return path