from fastapi import APIRouter
from app.rag.rag_service import RAGService
from app.models.schemas import AskRequest, AskResponse, IndexRequest, IndexResponse

print("6. routes.py started", flush=True)
router = APIRouter()

rag_service = None

def get_rag_service():
    global rag_service

    if rag_service is None:
        print("7. before RAGService", flush=True)
        rag_service = RAGService()
        print("8. after RAGService", flush=True)

    return rag_service

@router.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "TLDW AI",
        "version": "1.0.0"
    }

@router.post("/index", response_model = IndexResponse)
def index(request: IndexRequest):
    rag = get_rag_service()
    result = rag.index(request.youtube_url)
    
    return IndexResponse(
        video_id=result.video_id,
        from_cache=result.from_cache,
    )

@router.post("/ask", response_model = AskResponse)
def ask(request: AskRequest):
    rag = get_rag_service()
    answer, suggestions = rag.ask(
        request.youtube_url,
        request.question,
    )

    return AskResponse(
        answer=answer,
        suggestions=suggestions
    )