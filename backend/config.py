from pathlib import Path

SUPPORTED_LANGUAGES = ["en", "hi", "fr"]

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

EMBEDDING_MODEL = "intfloat/multilingual-e5-base"

DEVICE = "cpu"

BASE_DIR = Path(__file__).resolve().parent

CHROMA_PATH = BASE_DIR / "storage" / "chroma"

RETRIEVAL_K = 5
MMR_LAMBDA = 0.5

GEMINI_MODEL = "gemini-3.1-flash-lite"