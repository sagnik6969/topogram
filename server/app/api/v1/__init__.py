from fastapi import APIRouter
from .endpoints.diagrams import router as diagrams_router


router = APIRouter(prefix="/v1")
router.include_router(diagrams_router)

__all__ = ["router"]
