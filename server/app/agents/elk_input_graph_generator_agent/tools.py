import json
import os
from langchain.tools import tool
import logging

# Determine the path to the icons file
# This file: server/app/agents/elk_input_graph_generator_agent/tools.py
# Target: server/app/assets/aws_icons.json
BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ICONS_FILE_PATH = os.path.join(BASE_PATH, "assets", "aws_icons.json")


logger = logging.getLogger(__name__)


class IconLoadingError(Exception):
    """Raised when there is an issue loading the AWS icons file."""

    pass


# Load icons data once at module level
try:
    with open(ICONS_FILE_PATH, "r") as f:
        _ICONS_DATA = json.load(f)
except Exception as e:
    logger.error(f"Error loading AWS icons from {ICONS_FILE_PATH}: {e}")
    raise IconLoadingError(f"Failed to load AWS icons file at {ICONS_FILE_PATH}") from e


@tool
def search_aws_icons(search_string: str) -> list:
    """
    Search for AWS icons.

    It accepts a search string as input and returns an array of jsons (dicts)
    containing 'id' and 'name' fields for icons where the search string
    is found in either the id or name.

    Args:
        search_string (str): The search query.

    Returns:
        list: A list of dicts with keys "id" and "name".
    """
    search_term = search_string.lower()
    results = []

    for icon in _ICONS_DATA:
        # Check if search term is in id or name (case-insensitive)
        if (
            search_term in icon.get("id", "").lower()
            or search_term in icon.get("name", "").lower()
        ):
            results.append({"id": icon.get("id"), "name": icon.get("name")})

    return results[:5]
