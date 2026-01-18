from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


class Edge(BaseModel):
    id: str = Field(description="Unique id for the edge")
    sources: List[str] = Field(description="List of source node ids")
    targets: List[str] = Field(description="List of target node ids")


class Node(BaseModel):
    id: str = Field(description="Unique id for the node")
    text: Optional[str] = Field(
        default=None, description="Optional text content to be displayed on the node"
    )
    icon_id: Optional[str] = Field(
        default=None, description="Optional identifier for an icon to be displayed"
    )
    children: Optional[List[Node]] = Field(
        default=None,
        description="List of direct children nodes found inside this node. This structure is recursive.",
    )  # rebuild the model to update forward references for the recursive 'children' field


Node.model_rebuild()


class Graph(BaseModel):
    nodes: List[Node] = Field(description="List of nodes in the graph")
    edges: List[Edge] = Field(description="List of All the edges in the graph")
