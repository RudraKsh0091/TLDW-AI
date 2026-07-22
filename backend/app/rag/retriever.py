import logging

from langchain_chroma import Chroma
from langchain_core.documents import Document

from config import RETRIEVAL_K, MMR_LAMBDA

logger = logging.getLogger(__name__)

class DocumentRetriever:
    """
    Service responsible for retrieving relevant documents from the vector store.
    """
    
    def __init__(self, vector_store: Chroma):
        self.retriever = vector_store.as_retriever(
            search_type = 'mmr',
            search_kwargs = {
                'k' : RETRIEVAL_K,
                'lambda_mult' : MMR_LAMBDA
            }
        )
        
    def retrieve(self, question: str) -> list[Document]:
        """
        Retrieve relevant Documents for a user query
        """
        
        logger.info("Retrieving relevant documents")
        
        return self.retriever.invoke(question)