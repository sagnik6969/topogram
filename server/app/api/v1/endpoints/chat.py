from fastapi import APIRouter, Depends, Request
from app.api.v1.schemas.chat import ChatRequest
from app.services.chart_service import get_chat_service, ChatService
from app.config.settings import settings
from app.core.rate_limit import limiter
router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
@limiter.limit("; ".join(settings.DEFAULT_CHAT_RATE_LIMITS_PER_USER))
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


@router.get("/")
async def get_all_chats(
    request: Request,
    limit: int = 20,
    offset: int = 0,
    chat_service: ChatService = Depends(get_chat_service),
):
    return await chat_service.get_user_chats(
        user_id=request.state.uid, limit=limit, offset=offset
    )


@router.get("/{thread_id}")
async def get_chat(
    thread_id: str,
    request: Request,
    chat_service: ChatService = Depends(get_chat_service),
):
    return await chat_service.get_chat(thread_id=thread_id, user_id=request.state.uid)


