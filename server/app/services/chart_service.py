from uuid import uuid4
from app.services.diagram_service import DiagramService, get_diagram_service
from fastapi import Depends
from app.db.repositories.chat_repository import LanggraphCheckpoints
from fastapi import HTTPException
from utils.serialize_checkpoint import serialize_checkpoint


class ChatService:
    def __init__(self, diagram_service: DiagramService):
        self.diagram_service = diagram_service

    async def chat(
        self, user_message: str, thread_id: str | None, user_id: str
    ) -> dict:
        if thread_id:
            checkpoint = LanggraphCheckpoints(session_id=thread_id, user_id=user_id)
            if not checkpoint.exists():
                raise HTTPException(status_code=404, detail="Chat thread not found")

            checkpoint.store_checkpoint({"messages": []})
        else:
            new_thread_id = str(uuid4())

            checkpoint = LanggraphCheckpoints(session_id=new_thread_id, user_id=user_id)
            checkpoint.initialize_session()

        checkpoint.add_message(role="user", content=user_message)

        (
            excalidraw,
            agent_response,
        ) = await self.diagram_service.generate_excalidraw_from_description(
            checkpoint.get_checkpoint()
        )
        checkpoint.store_checkpoint(serialize_checkpoint(agent_response))
        return excalidraw


def get_chat_service(
    diagram_service: DiagramService = Depends(get_diagram_service),
) -> ChatService:
    return ChatService(diagram_service)
