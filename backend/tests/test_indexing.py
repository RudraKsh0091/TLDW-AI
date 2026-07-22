from app.rag.indexing import IndexingService

service = IndexingService()

db = service.index_video(
    "https://www.youtube.com/watch?v=J5_-l7WIO_w"
)

print(db.vector_store._collection.count())