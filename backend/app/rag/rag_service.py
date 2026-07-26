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
    
    def index(self, youtube_url: str):
        return self.indexing_service.index_video(youtube_url)
        
    def ask(self, youtube_url: str, question: str) -> str:
        vector_store = self.indexing_service.get_vector_store(
            youtube_url
        )

        retriever = DocumentRetriever(vector_store)

        qa_chain = QAChain(
            retriever,
            self.llm,
        )

        return qa_chain.ask(question)