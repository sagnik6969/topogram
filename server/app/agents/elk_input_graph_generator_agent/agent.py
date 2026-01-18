from langchain.agents import create_agent
from app.config.settings import settings

agent = create_agent(model=settings.DEFAULT_CHAT_MODEL_NAME, tools=[], verbose=True)
