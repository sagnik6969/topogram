from google.cloud import firestore
import uuid


class LanggraphCheckpoints:
    def __init__(self, session_id: str = None, user_id: str = "anonymous"):
        self.db = firestore.Client()
        self.user_id = user_id
        # If no session provided, generate a new one
        self.session_id = session_id if session_id else str(uuid.uuid4())

        # References
        self.session_ref = self.db.collection("chat_sessions").document(self.session_id)

    def exists(self) -> bool:
        """Checks if the session document exists."""
        return self.session_ref.get().exists

    def initialize_session(self):
        """Creates the session document if it doesn't exist."""
        if not self.session_ref.get().exists:
            self.session_ref.set(
                {
                    "user_id": self.user_id,
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "updated_at": firestore.SERVER_TIMESTAMP,
                    "checkpoint": None,
                }
            )

    def store_checkpoint(self, checkpoint_data: dict):
        """Stores checkpoint data in the session document."""
        self.session_ref.update({"checkpoint": checkpoint_data})

    def add_message(self, role: str, content: str):
        self.session_ref.update(
            {
                "checkpoint.messages": firestore.ArrayUnion(
                    [{"role": role, "content": content}]
                )
            }
        )

    def get_checkpoint(self) -> dict | None:
        """Retrieves checkpoint data from the session document."""
        doc = self.session_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return data.get("checkpoint", None)
        return None


class ChatRepository:
    def __init__(self):
        self.db = firestore.Client()
        self.collection = self.db.collection("chat_sessions")

    def get_user_chats(
        self, user_id: str, limit: int = 20, offset: int = 0
    ) -> list[dict]:
        """Fetches all chats for a given user with pagination."""
        query = (
            self.collection.where(filter=firestore.FieldFilter("user_id", "==", user_id))
            .order_by("created_at", direction=firestore.Query.DESCENDING)
            .limit(limit)
            .offset(offset)
        )
        docs = query.stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]

    def get_chat(self, thread_id: str, user_id: str) -> dict | None:
        """Fetches a specific chat by ID if it belongs to the user."""
        doc_ref = self.collection.document(thread_id)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            if data.get("user_id") == user_id:
                return {"id": doc.id, **data}
        return None
