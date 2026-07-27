import logging

from langchain_huggingface import HuggingFaceEmbeddings

from config import EMBEDDING_MODEL, DEVICE

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Service Responsible for creating the embedding model
    """
    
    def __init__(self):
        logger.info("Loading Embedding Model...")
        print("Loading Embedding Model...", flush=True)
        
        self.embedding_model = HuggingFaceEmbeddings(
            model_name = EMBEDDING_MODEL,
            model_kwargs = {
                "device": DEVICE
            },
            encode_kwargs = {
                "normalize_embeddings": True
            }
        )
        
        logger.info("Embedding model loaded successfully.")
        print("Embedding Model Loaded", flush=True)
        
    def get_embedding_model(self) -> HuggingFaceEmbeddings:
        """
        Returns the embedding Model
        """
        
        return self.embedding_model
        
        
    