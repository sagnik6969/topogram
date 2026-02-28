from langchain.chat_models import init_chat_model
from app.config.settings import settings
from langchain_cerebras import ChatCerebras

chat_model_name = settings.DEFAULT_CHAT_MODEL_NAME

if chat_model_name.startswith("cerebras:"):
    chat_model_name = chat_model_name.split("cerebras:")[1]

    default_chat_model = ChatCerebras(
        model=chat_model_name,
    )
else:
    default_chat_model = init_chat_model(
        model_name=chat_model_name,
    )
 

