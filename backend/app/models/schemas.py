from pydantic import BaseModel

class IndexRequest(BaseModel):
    youtube_url: str
    
class AskRequest(BaseModel):
    youtube_url: str
    question: str
    
class IndexResponse(BaseModel):
    video_id: str
    from_cache: bool

class AskResponse(BaseModel):
    answer: str
    
