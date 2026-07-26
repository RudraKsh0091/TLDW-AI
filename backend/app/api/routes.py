from fastapi import APIRouter
from app.rag.rag_service import RAGService
from app.models.schemas import AskRequest, AskResponse, IndexRequest, IndexResponse

router = APIRouter()
    
rag_service = RAGService()

@router.get("/")
def home_page():
    return {
        "message" : "Welcome to TLDW AI"
    }

@router.post("/index", response_model = IndexResponse)
def index(request: IndexRequest):
    result = rag_service.index(request.youtube_url)
    
    return IndexResponse(
        video_id=result.video_id,
        from_cache=result.from_cache,
    )

@router.post("/ask", response_model = AskResponse)
def ask(request: AskRequest):
    answer = rag_service.ask(
        request.youtube_url,
        request.question,
    )
    
    return AskResponse(answer = answer)