from langchain.agents import create_agent
from app.config.settings import settings
from app.agents.elk_input_graph_generator_agent.tools import search_aws_icons
from app.agents.elk_input_graph_generator_agent.schemas import Graph

agent = create_agent(
    model=settings.DEFAULT_CHAT_MODEL_NAME,
    tools=[search_aws_icons],
    verbose=True,
    response_format=Graph,
)
