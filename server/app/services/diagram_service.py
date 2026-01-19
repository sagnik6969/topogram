from typing import Dict, List, Any, TypedDict
from app.config.settings import settings
from uuid import uuid4
import httpx
import json
import os
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
    def __init__(self):
        base_path = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        icons_path = os.path.join(base_path, "app", "assets", "aws_icons.json")
        try:
            with open(icons_path, "r") as f:
                self.aws_icons = {icon["id"]: icon for icon in json.load(f)}
        except Exception:
            self.aws_icons = {}

    def _convert_elk_elements_to_excalidraw_elements(
        self,
        elk_elements: list[dict],
        files: dict,
        parent_x: float = 0,
        parent_y: float = 0,
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
                "text": elk_element.get("text"),
                "icon_id": elk_element.get("icon_id"),
                "shape": "rectangle",
            }
            excalidraw_elements_in_current_step = (
                self.convert_graph_node_to_excalidraw_elements(
                    node, x, y, height, width, files
                )
            )
            excalidraw_elements.extend(excalidraw_elements_in_current_step)

            child_elements = elk_element.get("children", [])
            if child_elements:
                excalidraw_elements.extend(
                    self._convert_elk_elements_to_excalidraw_elements(
                        child_elements, files, x, y
                    )
                )
        return excalidraw_elements

    def _convert_elk_edges_to_excalidraw_elements(
        self, elk_edges: list[dict]
    ) -> list[dict]:
        excalidraw_edges = []
        for edge in elk_edges:
            raw_points = []

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
                "roughness": 0,
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
                "endArrowhead": "arrow",
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
        files = {}
        excalidraw_elements = self._convert_elk_elements_to_excalidraw_elements(
            elk_json.get("children", []), files
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
            "files": files,
        }

    def convert_graph_node_to_excalidraw_elements(
        self,
        node: Node,
        x: int,
        y: int,
        height: int,
        width: int,
        files: dict,
    ) -> list[dict]:
        elements = []
        icon_id = node.get("icon_id")
        text_content = node.get("text")
        group_id = str(uuid4())

        # 1. Render Icon if available
        if icon_id and icon_id in self.aws_icons:
            icon_data = self.aws_icons[icon_id]
            file_id = str(uuid4())
            # Excalidraw expects "dataURL" in files
            files[file_id] = {
                "id": file_id,
                "dataURL": icon_data["url"],
                "mimeType": "image/svg+xml",
                "created": 1768110275345,  # Dummy timestamp
                "lastRetrieved": 1768110275345,
            }

            image_element = {
                "id": str(uuid4()),
                "type": "image",
                "x": x,  # Center horizontally (icon is 128x128)
                "y": y,  # Top aligned
                "width": 128,
                "height": 128,
                "angle": 0,
                "strokeColor": "transparent",
                "backgroundColor": "transparent",
                "fillStyle": "hachure",
                "strokeWidth": 1,
                "strokeStyle": "solid",
                "roughness": 0,
                "opacity": 100,
                "groupIds": [group_id],
                "frameId": None,
                "roundness": None,
                "seed": 926821016,
                "version": 66,
                "versionNonce": 750530792,
                "isDeleted": False,
                "boundElements": None,
                "updated": 1768110275345,
                "link": None,
                "locked": False,
                "fileId": file_id,
                "status": "saved",
                "scale": [1, 1],
            }
            elements.append(image_element)
        else:
            # Fallback shape if no icon
            shape = {
                "id": node["id"],
                "type": "rectangle",
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
                "roughness": 0,
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
            elements.append(shape)

        # 2. Render Text if available
        if text_content:
            text_element_id = str(uuid4())
            # For icon nodes, text is below the icon
            # Start Y for text = y + 128 (icon height) if icon exists, else middle
            # The user requested specific calculation based on logic:
            # width/height were pre-calculated in process_node.
            # If leaf node (icon present): width ~ 128+padding, height = 128+text_height+padding

            # Re-calculate text dimensions to position it
            font_size = settings.DEFAULT_EXCALIDRAW_ELEMENT_TEXT_FONT_SIZE
            line_height = settings.DEFAULT_EXCALIDRAW_ELEMENT_TEXT_LINE_HEIGHT

            # Using the pre-formatted text with newlines from process_node
            lines = text_content.split("\n")
            num_lines = len(lines)
            max_line_chars = max([len(line) for line in lines]) if lines else 0

            text_element_width = (
                max_line_chars
                * font_size
                * settings.DEFAULT_EXCALIDRAW_ELEMENT_TEXT_FONT_TO_WIDTH_RATIO
            )
            text_element_height = num_lines * font_size * line_height

            # Center text horizontally
            text_element_x = x

            if icon_id:
                # Place below icon (128px)
                text_element_y = y + 128
            else:
                # Center vertically in the box
                text_element_y = y

            text_element = {
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
                "roughness": 0,
                "opacity": 100,
                "groupIds": [group_id],
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
                "text": text_content,
                "fontSize": font_size,
                "fontFamily": settings.DEFAULT_EXCALIDRAW_ELEMENT_FONT_FAMILY,
                "textAlign": "center",
                "verticalAlign": "middle",
                "containerId": node["id"]
                if not icon_id
                else None,  # Only bind if it's inside a container shape
                "originalText": text_content,
                "autoResize": True,
                "lineHeight": line_height,
            }

            # If we created a fallback shape, bind text to it
            if not icon_id and len(elements) > 0:
                elements[0]["boundElements"] = [{"type": "text", "id": text_element_id}]

            elements.append(text_element)

        return elements

    def convert_agent_response_to_elk_json(self, agent_response: dict) -> dict:
        nodes = agent_response.get("nodes", [])
        edges = agent_response.get("edges", [])

        node_map = {}
        # First pass: create all nodes
        for node_data in nodes:
            node_map[node_data["id"]] = {
                "id": node_data["id"],
                "text": node_data.get("text"),
                "icon_id": node_data.get("icon_id"),
                "children": [],
            }

        # Second pass: build hierarchy
        non_root_ids = set()
        for node_data in nodes:
            parent_id = node_data["id"]
            children_ids = node_data.get("children_ids", [])
            for child_id in children_ids:
                if child_id in node_map:
                    node_map[parent_id]["children"].append(node_map[child_id])
                    non_root_ids.add(child_id)

        # Collect roots
        root_nodes = [node for nid, node in node_map.items() if nid not in non_root_ids]

        return {"id": "root", "children": root_nodes, "edges": edges}

    def generate_elk_json_input_using_agent(self, prompt: str) -> dict:
        agent_response: PartialElkGraph = elk_input_graph_generator_agent.invoke(
            {"messages": [{"role": "user", "content": prompt}]}
        )
        graph_dict = agent_response["structured_response"].model_dump(mode="json")

        elk_graph = self.convert_agent_response_to_elk_json(graph_dict)

        base_layout_options = {
            "elk.hierarchyHandling": "INCLUDE_CHILDREN",
            "elk.algorithm": "elk.layered",
            "nodePlacement.strategy": "BRANDES_KOEPF",
            "elk.layered.mergeEdges": False,
            "elk.direction": "RIGHT",
            "spacing.baseValue": 80,
            "elk.layered.crossingMinimization.forceNodeModelOrder": False,
            "elk.layered.considerModelOrder.strategy": "NODES_AND_EDGES",
            "elk.layered.unnecessaryBendpoints": True,
            "elk.layered.wrapping.multiEdge.improveCuts": True,
            "elk.layered.wrapping.multiEdge.improveWrappedEdges": True,
            "elk.layered.edgeRouting.selfLoopDistribution": "EQUALLY",
            "elk.layered.mergeHierarchyEdges": True,
        }

        elk_graph["layoutOptions"] = base_layout_options

        def process_node(node: dict):
            # Check if leaf (no children or empty children list)
            children = node.get("children")
            is_leaf = not children

            # 3. Each element should have padding
            # Remove padding from leaf nodes as per user request
            padding = 0 if is_leaf else 8
            node.setdefault("layoutOptions", {})
            node["layoutOptions"]["elk.padding"] = (
                f"[top={padding},left={padding},bottom={padding},right={padding}]"
            )

            if is_leaf:
                # 2. For each leaf node add its height and width.
                icon_dim = 128
                text = node.get("text")

                width = icon_dim
                height = icon_dim

                if text:
                    font_size = settings.DEFAULT_EXCALIDRAW_ELEMENT_TEXT_FONT_SIZE
                    # Text should be wrapped if it goes outside the icon width
                    max_width = icon_dim
                    char_width = (
                        font_size
                        * settings.DEFAULT_EXCALIDRAW_ELEMENT_TEXT_FONT_TO_WIDTH_RATIO
                    )
                    # avoid division by zero
                    chars_per_line = (
                        int(max_width / char_width) if char_width > 0 else 1
                    )

                    words = text.split()
                    lines = []
                    current_line = []
                    current_length = 0

                    for word in words:
                        word_len = len(word)
                        # space needed if not first word
                        needed = word_len + (1 if current_line else 0)

                        if current_length + needed <= chars_per_line:
                            current_line.append(word)
                            current_length += needed
                        else:
                            if current_line:
                                lines.append(" ".join(current_line))
                            current_line = [word]
                            current_length = word_len

                    if current_line:
                        lines.append(" ".join(current_line))

                    # Update text to include \n
                    node["text"] = "\n".join(lines)
                    num_lines = len(lines)

                    text_height = (
                        num_lines
                        * font_size
                        * settings.DEFAULT_EXCALIDRAW_ELEMENT_TEXT_LINE_HEIGHT
                    )

                    height += text_height

                # Add padding to dimensions as well
                node["width"] = width + (2 * padding)
                node["height"] = height + (2 * padding)

            else:
                # Recurse
                for child in children:
                    process_node(child)

        for node in elk_graph.get("children", []):
            process_node(node)

        return elk_graph

    def generate_elk_output_json(self, elk_graph: dict) -> dict:
        with httpx.Client() as client:
            response = client.post(
                settings.ELK_SERVICE_ENDPOINT, json={"jsonGraph": elk_graph}
            )
            response.raise_for_status()
            return response.json()

    def generate_excalidraw_from_description(self, description: str) -> dict:
        elk_input_graph = self.generate_elk_json_input_using_agent(description)
        elk_output_graph = self.generate_elk_output_json(elk_input_graph)
        excalidraw_json = self.convert_elk_json_to_excalidraw(elk_output_graph)
        return excalidraw_json
