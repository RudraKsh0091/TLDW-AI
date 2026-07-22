from app.rag.loader import TranscriptLoader
from app.rag.splitter import DocumentSplitter
from app.rag.embedding import EmbeddingService
from app.rag.vector_store import VectorStoreService

VIDEO_ID = "test_video"

loader = TranscriptLoader()
splitter = DocumentSplitter()
embedding_service = EmbeddingService()

vector_store = VectorStoreService(
    embedding_service.get_embedding_model()
)

documents = loader.load_transcript(
    "https://www.youtube.com/watch?v=J5_-l7WIO_w"
)

chunks = splitter.split_documents(documents)

db = vector_store.create_vector_store(
    chunks,
    VIDEO_ID,
)

print(db._collection.count())