from pydantic import BaseModel

class OpenAIRequest(BaseModel):
    topic: str
    network: str
    days: int
