from google.cloud import firestore
import uuid


class FirestoreChatHistory:
    def __init__(self, session_id: str = None, user_id: str = "anonymous"):
        self.db = firestore.Client()
        self.user_id = user_id
        # If no session provided, generate a new one
        self.session_id = session_id if session_id else str(uuid.uuid4())

        # References
        self.session_ref = self.db.collection("chat_sessions").document(self.session_id)
        self.messages_ref = self.session_ref.collection("messages")

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
                }
            )

    def add_message(self, role: str, content: str):
        """
        Adds a message to the history.
        role: 'user' or 'ai' (or 'system')
        """
        message_data = {
            "role": role,
            "content": content,
            "timestamp": firestore.SERVER_TIMESTAMP,
        }
        # Add to sub-collection
        self.messages_ref.add(message_data)

        # Update parent session timestamp for sorting active chats
        self.session_ref.update({"updated_at": firestore.SERVER_TIMESTAMP})

    def get_history(self, limit=10):
        """
        Fetches recent messages for context window.
        Returns a list of dicts: [{'role': 'user', 'content': '...'}, ...]
        """
        # Query: Order by timestamp descending (newest first) -> limit -> reverse back
        query = self.messages_ref.order_by(
            "timestamp", direction=firestore.Query.DESCENDING
        ).limit(limit)

        docs = query.stream()

        # We fetch newest first for efficiency, but list should be oldest->newest for the AI
        history = []
        for doc in docs:
            history.append(doc.to_dict())

        return history[::-1]  # Reverse to chronological order

    def delete_history(self):
        """Hard deletes all messages in the session (batched)."""
        batch = self.db.batch()
        docs = self.messages_ref.list_documents()

        for doc in docs:
            batch.delete(doc)

        batch.commit()
        self.session_ref.delete()
