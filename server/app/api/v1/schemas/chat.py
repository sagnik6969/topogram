from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    thread_id: str | None = None
    user_message: str = Field(..., max_length=500)
