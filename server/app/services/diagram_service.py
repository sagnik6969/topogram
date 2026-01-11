from typing import Dict, List, Any, TypedDict
from collections import deque
from config.settings import settings
import httpx
from uuid import uuid4


class DiagramType(TypedDict):
    type: str
    direction: str


class Node(TypedDict):
    id: str
    label: str | None
    shape: str


# Redefining Edge to handle 'from' keyword safely
Edge = TypedDict("Edge", {"from": str, "to": str, "type": str})


class Graph(TypedDict):
    diagramType: DiagramType
    nodes: Dict[str, Node]
    edges: List[Edge]
    metadata: Dict[str, Any]


class DiagramService:
    async def convert_mermaid_to_excalidraw(self, mermaid_code: str) -> dict:
        converted_mermaid_json = await self.convert_mermaid_to_json(mermaid_code)
        level_order_traversal = self.get_level_order_traversal(
            converted_mermaid_json,
            start_node_id=list(converted_mermaid_json["nodes"].keys())[0],
        )

        excalidraw_elements = []

        for level_index, level in enumerate(level_order_traversal):
            for node_index, node in enumerate(level):
                x = node_index * (settings.DEFAULT_EXCALIDRAW_ELEMENT_WIDTH + 50) + 50
                y = (
                    level_index * (settings.DEFAULT_EXCALIDRAW_ELEMENT_HEIGHT + 100)
                    + 50
                )
                excalidraw_elements = self.convert_graph_node_to_excalidraw_elements(
                    node,
                    x,
                    y,
                    settings.DEFAULT_EXCALIDRAW_ELEMENT_HEIGHT,
                    settings.DEFAULT_EXCALIDRAW_ELEMENT_WIDTH,
                )
                excalidraw_elements.extend(excalidraw_elements)

        return {
            "type": "excalidraw",
            "version": 2,
            "source": "http://localhost:5173",
            "elements": excalidraw_elements,
            "appState": {
                "gridSize": 20,
                "gridStep": 5,
                "gridModeEnabled": False,
                "viewBackgroundColor": "#ffffff",
                "lockedMultiSelections": {},
            },
            "files": {},
        }

    async def convert_mermaid_to_json(self, mermaid_code: str) -> Graph:
        url = settings.MERMAID_TO_JSON_SERVICE_ENDPOINT
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={"mermaid": mermaid_code})
            response.raise_for_status()
            graph_json = response.json()
            return graph_json

    def get_level_order_traversal(
        self, graph: Graph, start_node_id: str
    ) -> List[List[Node]]:
        if not graph or not start_node_id:
            return []

        nodes = graph.get("nodes", {})
        edges = graph.get("edges", [])

        # Build adjacency list
        adj = {}
        for edge in edges:
            u, v = edge.get("from"), edge.get("to")
            if u and v:
                if u not in adj:
                    adj[u] = []
                adj[u].append(v)

        queue = deque([(start_node_id, 0)])
        visited = {start_node_id}
        result = []

        while queue:
            node_id, level = queue.popleft()

            # Ensure result list is large enough
            if len(result) <= level:
                result.append([])

            if node_id in nodes:
                result[level].append(nodes[node_id])

            if node_id in adj:
                for neighbor in adj[node_id]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, level + 1))

        return result

    def convert_graph_node_to_excalidraw_elements(
        node: Node, x: int, y: int, height: int, width: int
    ) -> list[dict]:
        # Placeholder for actual conversion logic

        shape = {
            "id": node["id"],
            "type": node["shape"],
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "angle": 0,
            "strokeColor": settings.DEFAULT_EXCALIDRAW_ELEMENT_STROKE_COLOR,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "index": "a0",
            "roundness": {"type": 3},
            "seed": 926821016,
            "version": 66,
            "versionNonce": 750530792,
            "isDeleted": False,
            "updated": 1768110275345,
            "link": None,
            "locked": False,
        }

        if node["label"]:
            text_element_id = str(uuid4())
            text_element_width = (
                len(node["label"])
                * settings.DEFAULT_EXCALIDRAW_ELEMENT_TEXT_FONT_SIZE
                * settings.DEFAULT_EXCALIDRAW_ELEMENT_TEXT_FONT_TO_WIDTH_RATIO
            )
            text_element_height = (
                settings.DEFAULT_EXCALIDRAW_ELEMENT_TEXT_FONT_SIZE
                * settings.DEFAULT_EXCALIDRAW_ELEMENT_TEXT_LINE_HEIGHT
            )
            text_element_x = x + width / 2 - text_element_width / 2
            text_element_y = y + height / 2 - text_element_height / 2
            shape["boundElements"] = [{"type": "text", "id": text_element_id}]
            text = (
                {
                    "id": text_element_id,
                    "type": "text",
                    "x": text_element_x,
                    "y": text_element_y,
                    "width": text_element_width,
                    "height": text_element_height,
                    "angle": 0,
                    "strokeColor": settings.DEFAULT_EXCALIDRAW_ELEMENT_STROKE_COLOR,
                    "backgroundColor": "transparent",
                    "fillStyle": "solid",
                    "strokeWidth": 2,
                    "strokeStyle": "solid",
                    "roughness": 1,
                    "opacity": 100,
                    "groupIds": [],
                    "frameId": None,
                    "index": "a1",
                    "roundness": None,
                    "seed": 1644561560,
                    "version": 8,
                    "versionNonce": 1166842264,
                    "isDeleted": False,
                    "boundElements": None,
                    "updated": 1768110277987,
                    "link": None,
                    "locked": False,
                    "text": node["label"],
                    "fontSize": settings.DEFAULT_EXCALIDRAW_ELEMENT_TEXT_FONT_SIZE,
                    "fontFamily": settings.DEFAULT_EXCALIDRAW_ELEMENT_FONT_FAMILY,
                    "textAlign": "center",
                    "verticalAlign": "middle",
                    "containerId": node["id"],
                    "originalText": node["label"],
                    "autoResize": True,
                    "lineHeight": settings.DEFAULT_EXCALIDRAW_ELEMENT_TEXT_LINE_HEIGHT,
                },
            )
            return [shape, text]
        return [shape]
