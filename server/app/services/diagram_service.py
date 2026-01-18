from typing import Dict, List, Any, TypedDict
from app.config.settings import settings
from uuid import uuid4
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
        agent_response: PartialElkGraph = elk_input_graph_generator_agent.invoke({"messages": [{"role": "user", "content": prompt}]})
        print(f"DEBUG: agent_response type: {type(agent_response)}")
        print(f"DEBUG: agent_response keys: {agent_response.keys() if isinstance(agent_response, dict) else 'Not a dict'}")
        if isinstance(agent_response, dict) and "output" in agent_response:
             print(f"DEBUG: agent_response['output'] type: {type(agent_response['output'])}")
        
        # Determine how to extract the dict
        if isinstance(agent_response, dict):
            # Attempt to find the graph data
            if "output" in agent_response:
                # If output is the Graph object (unlikely for standard agent, but possible if structured)
                if hasattr(agent_response["output"], "model_dump"):
                    agent_response_dict = agent_response["output"].model_dump(mode="json")
                elif isinstance(agent_response["output"], dict):
                    agent_response_dict = agent_response["output"]
                else:
                    # It might be a string that needs parsing?
                    # But the previous error INVALID_ARGUMENT was during schema validation, so it probably constructs the object.
                    # Let's assume for now we just want to see the error.
                    agent_response_dict = agent_response # Fallback to fail
            else:
                 agent_response_dict = agent_response
        else:
            agent_response_dict = agent_response.model_dump(mode="json")
        
        # Reconstruct hierarchy from flat list of nodes and children_ids
        nodes_map = {n["id"]: n for n in agent_response_dict.get("nodes", [])}
        all_child_ids = set()
        
        for node in nodes_map.values():
            if "children_ids" in node:
                children_ids = node.pop("children_ids")
                node["children"] = []
                for child_id in children_ids:
                    if child_id in nodes_map:
                        node["children"].append(nodes_map[child_id])
                        all_child_ids.add(child_id)
        
        # Identify root nodes (those that are not children of any other node)
        root_nodes = [n for id, n in nodes_map.items() if id not in all_child_ids]
        
        # Replace 'nodes' with 'children' for ELK format compatibility (top-level nodes are 'children' of the graph)
        agent_response_dict["children"] = root_nodes
        if "nodes" in agent_response_dict:
            del agent_response_dict["nodes"]

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

        agent_response_dict["layoutOptions"] = base_layout_options

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

        for node in agent_response_dict.get("children", []):
            process_node(node)

        return agent_response_dict
