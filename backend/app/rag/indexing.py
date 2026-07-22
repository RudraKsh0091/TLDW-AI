import logging

from dataclasses import dataclass
from langchain_chroma import Chroma
from app.rag.loader import TranscriptLoader
from app.rag.splitter import DocumentSplitter
from app.rag.embedding import EmbeddingService
from app.rag.vector_store import VectorStoreService

logger = logging.getLogger(__name__)

from app.utils.youtube import extract_video_id

@dataclass
class IndexingResult:
    video_id: str
    vector_store: Chroma
    from_cache: bool
    
class IndexingService:
    def __init__(self):
        self.loader = TranscriptLoader()
        self.splitter = DocumentSplitter()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService(
            self.embedding_service.get_embedding_model()
        )
        
    def index_video(self, youtube_url: str):
        video_id = extract_video_id(youtube_url)
        logger.info(f"Indexing video {video_id}")
        
        if self.vector_store.vector_store_exists(video_id):
            logger.info("Vector store already exists.")
            db = self.vector_store.load_vector_store(video_id)
            return IndexingResult(
                video_id=video_id,
                vector_store=db,
                from_cache=True,
            )
        
        logger.info("Creating new vector store.")
        
        documents = self.loader.load_transcript(youtube_url)
        
        chunks = self.splitter.split_documents(documents)
        
        db = self.vector_store.create_vector_store(
            chunks,
            video_id,
        )
        
        return IndexingResult(
            video_id=video_id,
            vector_store=db,
            from_cache=True,
        )