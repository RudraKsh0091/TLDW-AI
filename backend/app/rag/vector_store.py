import logging
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from config import CHROMA_PATH

logger = logging.getLogger(__name__)

class VectorStoreService:
    """
    Service for creating and loading Chroma vector stores.
    """
    
    def __init__(self, embedding_model: HuggingFaceEmbeddings):
        self.embedding_model = embedding_model
        
    def _get_video_path(self, video_id: str) -> Path:
        return CHROMA_PATH / video_id
    
    def vector_store_exists(self, video_id: str) -> bool:
        return self._get_video_path(video_id).exists()
    
    def create_vector_store(self, documents: list[Document], video_id: str) -> Chroma:
        video_path = self._get_video_path(video_id)
        video_path.mkdir(
            parents=True,
            exist_ok=True,
        )
        
        db = Chroma.from_documents(
            documents=documents,
            embedding=self.embedding_model,
            persist_directory=str(video_path)
        )
        
        return db
    
    def load_vector_store(self, video_id: str):
        video_path = self._get_video_path(video_id)
        
        return Chroma(
            persist_directory=str(video_path),
            embedding_function=self.embedding_model
        )