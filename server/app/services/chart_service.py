from uuid import uuid4
from app.services.diagram_service import DiagramService, get_diagram_service
from fastapi import Depends
from app.db.repositories.chat_repository import LanggraphCheckpoints, ChatRepository
from fastapi import HTTPException
from utils.serialize_checkpoint import serialize_checkpoint


class ChatService:
    def __init__(self, diagram_service: DiagramService):
        self.diagram_service = diagram_service
        self.chat_repository = ChatRepository()

    async def chat(
        self, user_message: str, thread_id: str | None, user_id: str
    ) -> dict:
        if thread_id:
            checkpoint = LanggraphCheckpoints(session_id=thread_id, user_id=user_id)
            if not checkpoint.exists():
                raise HTTPException(status_code=404, detail="Chat thread not found")
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
        return {"excalidraw": excalidraw, "thread_id": checkpoint.session_id}

    async def get_user_chats(
        self, user_id: str, limit: int = 20, offset: int = 0
    ) -> list[dict]:
        return self.chat_repository.get_user_chats(user_id, limit, offset)

    async def get_chat(self, thread_id: str, user_id: str) -> dict:
        chat_data = self.chat_repository.get_chat(thread_id, user_id)
        if not chat_data:
            raise HTTPException(status_code=404, detail="Chat thread not found")
        # Ensure we return only serializable data or clean it up if necessary
        # The checkpoint field might contain complex objects if not serialized properly before storage
        # But we assume storage is JSON compatible as per repository code.
        return chat_data


def get_chat_service(
    diagram_service: DiagramService = Depends(get_diagram_service),
) -> ChatService:
    return ChatService(diagram_service)
