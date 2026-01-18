from fastapi import APIRouter, Depends
from app.services.diagram_service import DiagramService
from app.api.deps import get_diagram_service

router = APIRouter(prefix="/diagrams", tags=["Diagrams"])


@router.post("/convert/elk_to_excalidraw")
async def convert_elk_to_excalidraw(
    elk_json: dict,
    diagram_service: DiagramService = Depends(get_diagram_service),
) -> dict:
    return diagram_service.convert_elk_json_to_excalidraw(elk_json)


@router.post("/generate/elk_input_graph")
async def generate_elk_input_graph(
    description: str,
    diagram_service: DiagramService = Depends(get_diagram_service),
) -> dict:
    return diagram_service.generate_elk_json_input_using_agent(description)
