from pydantic import BaseModel


class ConvertMermaidToExcalidrawRequest(BaseModel):
    mermaid_code: str


class ConvertMermaidToExcalidrawResponse(BaseModel):
    elements: list
    appState: dict
    type: str
    version: int
    source: str
    files: dict
