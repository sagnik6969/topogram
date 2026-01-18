from langchain.agents import create_agent
from app.config.settings import settings
from app.agents.elk_input_graph_generator_agent.tools import search_aws_icons
from app.agents.elk_input_graph_generator_agent.schemas import Graph
from app.agents.elk_input_graph_generator_agent.prompts import SYSTEM_PROMPT


agent = create_agent(
    model=settings.DEFAULT_CHAT_MODEL_NAME,
    tools=[search_aws_icons],
    response_format=Graph,
    system_prompt=SYSTEM_PROMPT,
)
