import customtkinter as ctk

from app.modules.documents.services.document_service import DocumentService



class DocumentsWindow(ctk.CTkToplevel):


    def __init__(self, parent=None, project_path=None):

        super().__init__(parent)


        self.project_path = project_path


        self.service = DocumentService(
            project_path
        )


        self.title(
            "Documents Module"
        )


        self.geometry(
            "700x450"
        )


        self.create_ui()



    def create_ui(self):


        title = ctk.CTkLabel(
            self,
            text="📄 Documents Manager",
            font=("Arial", 28, "bold")
        )


        title.pack(
            pady=30
        )



        self.documents_label = ctk.CTkLabel(
            self,
            text=self.get_documents_text(),
            font=("Arial", 16)
        )


        self.documents_label.pack(
            pady=20
        )



        button = ctk.CTkButton(
            self,
            text="Create Document",
            command=self.create_document
        )


        button.pack(
            pady=30
        )



    def get_documents_text(self):


        documents = (
            self.service.list_documents()
        )


        if not documents:

            return "No documents"



        return "\n".join(
            documents
        )



    def create_document(self):


        self.service.create_document(
            "NEW_DOCUMENT",
            "# New Project Forge Document"
        )


        self.documents_label.configure(
            text=self.get_documents_text()
        )