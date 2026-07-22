from app.rag.loader import TranscriptLoader

loader = TranscriptLoader()

docs = loader.load_transcript(
    "https://www.youtube.com/watch?v=J5_-l7WIO_w"
)

print(len(docs))
print(docs[0].page_content[:500])
print(docs[0].metadata)