import logging

from app.rag.indexing import IndexingService
from app.rag.llm import LLMService
from app.rag.qa_chain import QAChain
from app.rag.retriever import DocumentRetriever
from langchain_core.output_parsers import StrOutputParser

logger = logging.getLogger(__name__)

class RAGService:
    
    def __init__(self):
        self.indexing_service = IndexingService()
        self.llm = LLMService().get_llm()
    
    def index(self, youtube_url: str):
        return self.indexing_service.index_video(youtube_url)
        
    def ask(self, youtube_url: str, question: str):
        vector_store = self.indexing_service.get_vector_store(
            youtube_url
        )

        retriever = DocumentRetriever(vector_store)

        qa_chain = QAChain(
            retriever,
            self.llm,
        )

        answer = qa_chain.ask(question)

        prompt = f"""
        Generate exactly 3 short follow-up questions a user might ask after reading this answer.

        Answer:
        {answer}

        Rules:
        - One question per line
        - No numbering
        - No bullet points
        - Maximum 12 words each
        """

        suggestions_chain = self.llm | StrOutputParser()
        raw = suggestions_chain.invoke(prompt)
        
        suggestions = [
            line.strip()
            for line in raw.splitlines()
            if line.strip()
        ][:3]

        return answer, suggestions