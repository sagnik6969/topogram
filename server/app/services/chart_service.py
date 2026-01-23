from uuid import uuid4
from app.services.diagram_service import DiagramService, get_diagram_service
from fastapi import Depends
from app.db.repositories.chat_repository import FirestoreChatHistory
from fastapi import HTTPException


class ChatService:
    def __init__(self, diagram_service: DiagramService):
        self.diagram_service = diagram_service

    async def chat(
        self, user_message: str, thread_id: str | None, user_id: str
    ) -> dict:
        if thread_id:
            chat_history = FirestoreChatHistory(session_id=thread_id, user_id=user_id)
            if not chat_history.exists():
                raise HTTPException(status_code=404, detail="Chat thread not found")

            chat_history.add_message(role="user", content=user_message)

            agent_response = (
                await self.diagram_service.generate_excalidraw_from_description(
                    chat_history.get_history(limit=100)
                )
            )

            chat_history.add_message(role="ai", content=str(agent_response))

        if not thread_id:
            new_thread_id = str(uuid4())

            db_thread = FirestoreChatHistory(session_id=new_thread_id, user_id=user_id)
            db_thread.initialize_session()
            db_thread.add_message(role="user", content=user_message)

            agent_response = (
                await self.diagram_service.generate_excalidraw_from_description(
                    db_thread.get_history(limit=100)
                )
            )
            db_thread.add_message(role="ai", content=str(agent_response))

        return agent_response


def get_chat_service(
    diagram_service: DiagramService = Depends(get_diagram_service),
) -> ChatService:
    return ChatService(diagram_service)
