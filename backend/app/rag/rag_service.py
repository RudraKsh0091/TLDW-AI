import logging

from app.rag.indexing import IndexingService
from app.rag.llm import LLMService
from app.rag.qa_chain import QAChain
from app.rag.retriever import DocumentRetriever

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.indexing_service = IndexingService()
        self.llm = LLMService().get_llm()
        
    def ask(self, youtube_url: str, question: str) -> str:
        result = self.indexing_service.index_video(youtube_url)
        
        retriever = DocumentRetriever(
            result.vector_store
        )
        
        qa_chain = QAChain(
            retriever,
            self.llm,
        )
        
        return qa_chain.ask(question)
    
    