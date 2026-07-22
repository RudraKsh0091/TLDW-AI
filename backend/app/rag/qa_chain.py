import logging

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models.chat_models import BaseChatModel

logger = logging.getLogger(__name__)

from app.rag.prompts import QA_PROMPT

class QAChain:
    """
    Coordinates retrieval and answer generation.
    """
    
    def __init__(self, retriever, llm: BaseChatModel):
        self.retriever = retriever
        self.chain = QA_PROMPT | llm | StrOutputParser()
        
    def _build_context(self, documents: list[Document]) -> str:
        return "\n\n".join(
            doc.page_content
            for doc in documents
        )
    
    def ask(self, question: str) -> str:
        documents = self.retriever.retrieve(question)
        
        if not documents:
            return "I couldn't find any relevant information in the transcript."
        
        context = self._build_context(documents)
        
        logger.info("Generating answer using Gemini.")
        
        return self.chain.invoke({
            "context": context,
            "question": question,
        })