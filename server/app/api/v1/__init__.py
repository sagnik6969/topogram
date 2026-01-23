from fastapi import APIRouter
from .endpoints.diagrams import router as diagrams_router
from .endpoints.chat import router as chat_router

router = APIRouter(prefix="/v1")
router.include_router(diagrams_router)
router.include_router(chat_router)

__all__ = ["router"]
