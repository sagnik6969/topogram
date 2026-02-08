from typing import Any


def serialize_checkpoint(checkpoint_data: Any) -> dict:
    """Serializes checkpoint data for storage."""
    # Implement any necessary serialization logic here
    if checkpoint_data is None:
        return None

    serialized = {}
    for key, value in checkpoint_data.items():
        if key == "messages" and isinstance(value, list):
            # Serialize message objects
            serialized[key] = []
            for msg in value:
                if hasattr(msg, "dict"):
                    # LangChain message objects have a dict() method
                    message_dict: dict = msg.dict()
                    message_dict.get("additional_kwargs", {}).pop(
                        "__gemini_function_call_thought_signatures__", None
                    )
                    serialized[key].append(message_dict)
                elif isinstance(msg, dict):
                    serialized[key].append(msg)
                else:
                    # Fallback: convert to string representation
                    serialized[key].append(
                        {"content": str(msg), "type": type(msg).__name__}
                    )
        elif key == "structured_response":
            serialized[key] = value.model_dump(mode="json")
        else:
            serialized[key] = value

    return serialized
