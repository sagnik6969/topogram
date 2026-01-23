from fastapi import APIRouter, Depends, Request
from app.api.v1.schemas.chat import ChatRequest
from app.services.chart_service import get_chat_service, ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat_endpoint(
    request: Request,
    chat_request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
):
    return await chat_service.chat(
        user_message=chat_request.user_message,
        thread_id=chat_request.thread_id,
        user_id=request.state.uid,
    )
