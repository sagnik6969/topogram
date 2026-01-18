from langchain.chat_models import init_chat_model
from app.config.settings import settings

default_chat_model = init_chat_model(settings.DEFAULT_CHAT_MODEL_NAME, temperature=0.7)
