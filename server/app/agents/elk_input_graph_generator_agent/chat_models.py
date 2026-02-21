from langchain.chat_models import init_chat_model
from app.config.settings import settings
from langchain_cerebras import ChatCerebras

default_chat_model = ChatCerebras(
    model="llama-3.3-70b",
)

 

