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
    children_ids: List[str] = Field(
        default_factory=list,
        description="List of IDs of direct children nodes found inside this node. The actual child nodes should be listed in the top-level 'nodes' list.",
    )





class Graph(BaseModel):
    nodes: List[Node] = Field(description="List of nodes in the graph")
    edges: List[Edge] = Field(description="List of All the edges in the graph")
