from pydantic import ConfigDict, SecretStr
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "Diagram Copilot Main Backend Service"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORES_ALLOWED_ORIGINS: str
    MONGODB_URI: SecretStr
    ELK_SERVICE_ENDPOINT: str
    DEFAULT_EXCALIDRAW_ELEMENT_WIDTH: int = 150
    DEFAULT_EXCALIDRAW_ELEMENT_HEIGHT: int = 100
    DEFAULT_EXCALIDRAW_ELEMENT_STROKE_COLOR: str = "#1e1e1e"
    DEFAULT_EXCALIDRAW_ELEMENT_TEXT_FONT_SIZE: int = 20
    DEFAULT_EXCALIDRAW_ELEMENT_TEXT_LINE_HEIGHT: float = 1.25
    DEFAULT_EXCALIDRAW_ELEMENT_FONT_FAMILY: int = 5
    DEFAULT_EXCALIDRAW_ELEMENT_TEXT_FONT_TO_WIDTH_RATIO: float = 0.54
    DEFAULT_CHAT_MODEL_NAME: str = "google_genai:gemini-3-flash-preview"

    model_config = ConfigDict(env_file=".env", case_sensitive=True, extra="allow")


settings = Settings()
