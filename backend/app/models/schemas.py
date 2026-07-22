from pydantic import BaseModel

class IndexRequest(BaseModel):
    youtube_url: str
    
class AskRequest(BaseModel):
    youtube_url: str
    question: str
    
class IndexResponse(BaseModel):
    success: bool
    video_id: str

class AskResponse(BaseModel):
    answer: str
    
