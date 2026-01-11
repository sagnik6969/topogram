from typing import Dict, List, Any, TypedDict, Optional

class DiagramType(TypedDict):
    type: str
    direction: str

class Node(TypedDict):
    id: str
    label: str
    shape: str

# Redefining Edge to handle 'from' keyword safely
Edge = TypedDict("Edge", {
    "from": str,
    "to": str,
    "type": str
})

class Graph(TypedDict):
    diagramType: DiagramType
    nodes: Dict[str, Node]
    edges: List[Edge]
    metadata: Dict[str, Any]

class DiagramService:
    def __init__(self):
        pass

    @staticmethod
    def convert_mermaid_to_excalidraw(mermaid_code: str) -> str:
        excalidraw_code = f"Converted Excalidraw code from Mermaid:\n{mermaid_code}"
        return excalidraw_code

    @staticmethod
    def get_level_order_traversal(graph: Graph, start_node_id: str) -> List[List[Node]]:
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
        
        # BFS
        from collections import deque
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

