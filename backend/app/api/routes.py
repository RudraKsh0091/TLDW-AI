from fastapi import APIRouter
from app.rag.indexing import IndexingService
from app.rag.llm import LLMService
from app.rag.retriever import DocumentRetriever
from app.rag.qa_chain import QAChain
from app.models.schemas import IndexRequest, IndexResponse, AskRequest, AskResponse

router = APIRouter()

indexing_service = IndexingService()
llm_service = LLMService()

@router.post("/index")
def index_video(request: IndexRequest):
    result = indexing_service.index_video(
        request.youtube_url
    )
    
    return IndexResponse(
        success=True,
        video_id=result.video_id,
    )
    
@router.post("/ask")
def ask_question(request: AskRequest):
    result = indexing_service.index_video(request.youtube_url)
    
    retriever = DocumentRetriever(result.vector_store)
    
    qa = QAChain(
        retriever,
        llm_service.get_llm(),
    )
    
    answer = qa.ask(request.question)
    
    return AskResponse(
        answer = answer
    )
    
