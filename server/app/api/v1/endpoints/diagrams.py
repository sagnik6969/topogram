from fastapi import APIRouter, Depends
from app.schemas.diagrams import (
    ConvertMermaidToExcalidrawRequest,
    ConvertMermaidToExcalidrawResponse,
)
from app.services.diagram_service import DiagramService
from app.api.deps import get_diagram_service

router = APIRouter(prefix="/diagrams", tags=["Diagrams"])


@router.post(
    "/convert/mermaid-to-excalidraw", response_model=ConvertMermaidToExcalidrawResponse
)
async def convert_mermaid_to_excalidraw(
    request: ConvertMermaidToExcalidrawRequest,
    diagram_service: DiagramService = Depends(get_diagram_service),
) -> ConvertMermaidToExcalidrawResponse:
    return await diagram_service.convert_mermaid_to_excalidraw(request.mermaid_code)
