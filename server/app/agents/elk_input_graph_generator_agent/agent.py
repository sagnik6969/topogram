from langchain.agents import create_agent
from app.config.settings import settings
from app.agents.elk_input_graph_generator_agent.tools import search_aws_icons
from app.agents.elk_input_graph_generator_agent.schemas import Graph
from app.agents.elk_input_graph_generator_agent.prompts import SYSTEM_PROMPT
from typing import Any
from app.agents.elk_input_graph_generator_agent.chat_models import default_chat_model
from langchain.agents.structured_output import ToolStrategy

agent = create_agent(
    model=default_chat_model,
    tools=[search_aws_icons],
    response_format=ToolStrategy(Graph),
    system_prompt=SYSTEM_PROMPT,
)