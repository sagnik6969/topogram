from typing import Dict, List, Any, TypedDict
from collections import deque
from app.config.settings import settings
import httpx
from uuid import uuid4
from app.exceptions.diagrams import MermaidConversionError
from app.constants.diagrams import mermaid_to_excalidraw_shape_map
from app.agents.elk_input_graph_generator_agent.agent import (
    agent as elk_input_graph_generator_agent,
)
from app.agents.elk_input_graph_generator_agent.schemas import Graph as PartialElkGraph


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
                excalidraw_elements_in_current_step = (
                    self.convert_graph_node_to_excalidraw_elements(
                        node,
                        x,
                        y,
                        settings.DEFAULT_EXCALIDRAW_ELEMENT_HEIGHT,
                        settings.DEFAULT_EXCALIDRAW_ELEMENT_WIDTH,
                    )
                )
                excalidraw_elements.extend(excalidraw_elements_in_current_step)

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
            try:
                response = await client.post(url, json={"diagram": mermaid_code})
                response.raise_for_status()
                graph_json = response.json()
                return graph_json
            except httpx.HTTPError as e:
                raise MermaidConversionError(
                    response.json() if response else str(e),
                    response.status_code if response else 500,
                )

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

    def map_mermaid_shape_to_excalidraw(self, mermaid_shape: str) -> str:
        return mermaid_to_excalidraw_shape_map.get(mermaid_shape, "rectangle")

    def _convert_elk_elements_to_excalidraw_elements(
        self, elk_elements: list[dict], parent_x: float = 0, parent_y: float = 0
    ) -> list[dict]:
        excalidraw_elements = []

        for elk_element in elk_elements:
            if "offset" in elk_element:
                x = elk_element["offset"]["posX"]
                y = elk_element["offset"]["posY"]
            else:
                x = parent_x + elk_element.get("x", 0)
                y = parent_y + elk_element.get("y", 0)

            width = elk_element.get("width", 0)
            height = elk_element.get("height", 0)
            node = {
                "id": elk_element["id"],
                "label": None,
                "shape": "rectangle",
            }
            excalidraw_elements_in_current_step = (
                self.convert_graph_node_to_excalidraw_elements(
                    node, x, y, height, width
                )
            )
            excalidraw_elements.extend(excalidraw_elements_in_current_step)

            child_elements = elk_element.get("children", [])
            if child_elements:
                excalidraw_elements.extend(
                    self._convert_elk_elements_to_excalidraw_elements(
                        child_elements, x, y
                    )
                )
        return excalidraw_elements

    def _convert_elk_edges_to_excalidraw_elements(
        self, elk_edges: list[dict]
    ) -> list[dict]:
        excalidraw_edges = []
        for edge in elk_edges:
            raw_points = edge.get("points", [])
            if not raw_points and "sections" in edge:
                for section in edge.get("sections", []):
                    raw_points.append(section["startPoint"])
                    raw_points.extend(section.get("bendPoints", []))
                    raw_points.append(section["endPoint"])

            if not raw_points:
                continue

            start_point = raw_points[0]
            start_x = start_point["x"]
            start_y = start_point["y"]

            processed_points = [
                [p["x"] - start_x, p["y"] - start_y] for p in raw_points
            ]

            xs = [p[0] for p in processed_points]
            ys = [p[1] for p in processed_points]
            width = max(xs) - min(xs)
            height = max(ys) - min(ys)

            edge_data = edge.get("edgeData", {})
            end_arrowhead = (
                "arrow" if edge_data.get("arrowTypeEnd") == "arrow_point" else None
            )

            excalidraw_edge = {
                "id": edge.get("id", str(uuid4())),
                "type": "arrow",
                "x": start_x,
                "y": start_y,
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
                "roundness": None,
                "seed": 2052841052,
                "version": 1,
                "versionNonce": 0,
                "isDeleted": False,
                "boundElements": None,
                "updated": 1768666473949,
                "link": None,
                "locked": False,
                "points": processed_points,
                "startBinding": None,
                "endBinding": None,
                "startArrowhead": None,
                "endArrowhead": end_arrowhead,
                "elbowed": True,
            }

            if edge.get("sources"):
                excalidraw_edge["startBinding"] = {
                    "elementId": edge["sources"][0],
                    "mode": "orbit",
                    "fixedPoint": None,
                }

            if edge.get("targets"):
                excalidraw_edge["endBinding"] = {
                    "elementId": edge["targets"][0],
                    "mode": "orbit",
                    "fixedPoint": None,
                }

            excalidraw_edges.append(excalidraw_edge)

        return excalidraw_edges

    def convert_elk_json_to_excalidraw(self, elk_json: dict) -> dict:
        excalidraw_elements = self._convert_elk_elements_to_excalidraw_elements(
            elk_json.get("children", [])
        )
        excalidraw_elements.extend(
            self._convert_elk_edges_to_excalidraw_elements(elk_json.get("edges", []))
        )

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

    def convert_graph_node_to_excalidraw_elements(
        self, node: Node, x: int, y: int, height: int, width: int
    ) -> list[dict]:
        shape = {
            "id": node["id"],
            "type": self.map_mermaid_shape_to_excalidraw(node["shape"]),
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
            text = {
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
            }
            return [shape, text]
        return [shape]

    def generate_elk_json_input_using_agent(self, prompt: str) -> dict:
        agent_response: PartialElkGraph = elk_input_graph_generator_agent.invoke(prompt)
        agent_response_dict = agent_response.model_dump(mode="json")
        return agent_response_dict
