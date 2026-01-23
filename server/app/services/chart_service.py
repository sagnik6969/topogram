from app.db.models import UserThread
from uuid import uuid4
from app.services.diagram_service import DiagramService, get_diagram_service
from fastapi import Depends


class ChatService:
    def __init__(self, diagram_service: DiagramService):
        self.diagram_service = diagram_service

    async def chat(
        self, user_message: str, thread_id: str | None, user_id: str
    ) -> dict:
        if not thread_id:
            new_thread_id = str(uuid4())

            db_thread = UserThread(
                user_id=user_id, thread_id=new_thread_id, title="Test"
            )
            await db_thread.insert()

            agent_response = (
                await self.diagram_service.generate_excalidraw_from_description(
                    new_thread_id, user_message
                )
            )

        return agent_response


def get_chat_service(
    diagram_service: DiagramService = Depends(get_diagram_service),
) -> ChatService:
    return ChatService(diagram_service)
