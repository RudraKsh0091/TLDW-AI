from app.rag.loader import TranscriptLoader
from app.rag.splitter import DocumentSplitter

loader = TranscriptLoader()
splitter = DocumentSplitter()

documents = loader.load_transcript(
    "https://www.youtube.com/watch?v=J5_-l7WIO_w"
)

chunks = splitter.split_documents(documents)

print(f"Original Documents : {len(documents)}")
print(f"Chunks : {len(chunks)}")

print()

print(chunks[0].page_content)

print()

print(chunks[0].metadata)