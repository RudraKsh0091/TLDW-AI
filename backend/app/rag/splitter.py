from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_SIZE, CHUNK_OVERLAP

class DocumentSplitter:
    """
    Service for splitting documents into smaller chunks.
    """

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

    def split_documents(self, documents: list[Document]) -> list[Document]:
        """
        Split documents into smaller chunks.

        Args:
            documents: List of LangChain Documents.

        Returns:
            List of chunked Documents.
        """

        return self.splitter.split_documents(documents)