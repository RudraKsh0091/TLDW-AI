from app.rag.embeddings import EmbeddingService

embedding_service = EmbeddingService()

embedding_model = embedding_service.get_embedding_model()

print(embedding_model)