from app.rag.loader import TranscriptLoader
from app.rag.splitter import DocumentSplitter
from app.rag.embedding import EmbeddingService
from app.rag.vector_store import VectorStoreService
from app.rag.retriever import DocumentRetriever

url = "https://www.youtube.com/watch?v=J5_-l7WIO_w"

loader = TranscriptLoader()
splitter = DocumentSplitter()
embedding_service = EmbeddingService()

documents = loader.load_transcript(url)
chunks = splitter.split_documents(documents)

vector_store = VectorStoreService(
    embedding_service.get_embedding_model()
)

db = vector_store.create_vector_store(
    chunks,
    "test_video",
)

retriever = DocumentRetriever(db)

results = retriever.retrieve(
    "What is this video about?"
)

for i, doc in enumerate(results, start=1):
    print(f"\nChunk {i}")
    print("-" * 50)
    print(doc.page_content[:300])