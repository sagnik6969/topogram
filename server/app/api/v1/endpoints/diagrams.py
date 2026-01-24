from fastapi import APIRouter, Depends
from app.services.diagram_service import DiagramService
from app.services.diagram_service import get_diagram_service
from app.agents.elk_input_graph_generator_agent.agent import agent

router = APIRouter(prefix="/diagrams", tags=["Diagrams"])


@router.post("/generate/test-agent")
async def generate_test_agent():
    test_chat_history = [
        {
            "role": "user",
            "content": "Create a diagram with an S3 bucket and a Lambda function.",
        }
    ]
    agent_response = await agent.ainvoke({"messages": test_chat_history})
    return agent_response


@router.post("/convert/elk_to_excalidraw")
async def convert_elk_to_excalidraw(
    elk_json: dict,
    diagram_service: DiagramService = Depends(get_diagram_service),
) -> dict:
    return diagram_service.convert_elk_json_to_excalidraw(elk_json)


@router.post("/generate/excalidraw-from-description")
async def generate_excalidraw_from_description(
    description: str,
    diagram_service: DiagramService = Depends(get_diagram_service),
) -> dict:
    return diagram_service.generate_excalidraw_from_description(description)
