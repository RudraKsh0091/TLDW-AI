from langchain_google_genai import ChatGoogleGenerativeAI

from config import GEMINI_MODEL

class LLMService:
    """
    Service responsible for initializing the LLM
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model = GEMINI_MODEL,
            temperature = 0,
            thinking_level = 'low'
        )
        
    def get_llm(self):
        return self.llm