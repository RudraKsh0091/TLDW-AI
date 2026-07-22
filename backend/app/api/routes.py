from fastapi import APIRouter
from app.rag.rag_service import RAGService
from app.models.schemas import AskRequest, AskResponse

router = APIRouter()
    
rag_service = RAGService()


@router.post("/ask", response_model = AskResponse)
def ask(request: AskRequest):
    answer = rag_service.ask(
        request.youtube_url,
        request.question,
    )
    
    return AskResponse(answer = answer)