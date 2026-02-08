from pydantic import BaseModel, Field
from app.config.settings import settings

class ChatRequest(BaseModel):
    thread_id: str | None = None
    user_message: str = Field(..., max_length=settings.MAX_NUMBER_OF_CHARACTERS_IN_CHAT_MESSAGE)
