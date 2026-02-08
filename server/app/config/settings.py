from pydantic import ConfigDict, model_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydantic import SecretStr
from typing import List

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "Diagram Copilot Main Backend Service"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: SecretStr
    CORES_ALLOWED_ORIGINS: str
    ELK_SERVICE_ENDPOINT: str
    RATE_LIMIT_ENABLED: bool = True
    DEFAULT_APPLICATION_LEVEL_RATE_LIMITS_PER_USER: List[str] = []
    DEFAULT_CHAT_RATE_LIMITS_PER_USER: List[str] = []
    DEFAULT_RATE_LIMITS_FOR_ENDPOINTS: List[str] = []
    GLOBAL_CHAT_RATE_LIMITS: List[str] = []
    GLOBAL_CHAT_RATE_LIMIT_KEY: str = "global_chat_resource_limit"
    DEFAULT_EXCALIDRAW_ELEMENT_WIDTH: int = 150
    DEFAULT_EXCALIDRAW_ELEMENT_HEIGHT: int = 100
    DEFAULT_EXCALIDRAW_ELEMENT_STROKE_COLOR: str = "#1e1e1e"
    DEFAULT_EXCALIDRAW_ELEMENT_TEXT_FONT_SIZE: int = 20
    DEFAULT_EXCALIDRAW_ELEMENT_TEXT_LINE_HEIGHT: float = 1.25
    DEFAULT_EXCALIDRAW_ELEMENT_FONT_FAMILY: int = 5
    DEFAULT_EXCALIDRAW_ELEMENT_TEXT_FONT_TO_WIDTH_RATIO: float = 0.54
    DEFAULT_CHAT_MODEL_NAME: str = "google_genai:gemini-2.5-flash"
    AUTH_DISABLED: bool = (
        False  # Set to True to disable authentication (for testing/dev purposes only)
    )
    USER_ID_WHEN_AUTH_DISABLED: str = (
        "test-user"  # Default user ID to use when authentication is disabled
    )
    MAX_NUMBER_OF_CHARACTERS_IN_CHAT_MESSAGE: int = 2000

    model_config = ConfigDict(env_file=".env", case_sensitive=True, extra="allow")

    @model_validator(mode="after")
    def validate_rate_limit_settings(self):
        """Validate that rate limit settings are provided when rate limiting is enabled."""
        if self.RATE_LIMIT_ENABLED:
            missing_fields = []
            if (
                not self.DEFAULT_APPLICATION_LEVEL_RATE_LIMITS_PER_USER
                or len(self.DEFAULT_APPLICATION_LEVEL_RATE_LIMITS_PER_USER) == 0
            ):
                missing_fields.append("DEFAULT_APPLICATION_LEVEL_RATE_LIMITS_PER_USER")
            if (
                not self.DEFAULT_CHAT_RATE_LIMITS_PER_USER
                or len(self.DEFAULT_CHAT_RATE_LIMITS_PER_USER) == 0
            ):
                missing_fields.append("DEFAULT_CHAT_RATE_LIMITS_PER_USER")
            if (
                not self.DEFAULT_RATE_LIMITS_FOR_ENDPOINTS
                or len(self.DEFAULT_RATE_LIMITS_FOR_ENDPOINTS) == 0
            ):
                missing_fields.append("DEFAULT_RATE_LIMITS_FOR_ENDPOINTS")
            if (
                not self.GLOBAL_CHAT_RATE_LIMITS
                or len(self.GLOBAL_CHAT_RATE_LIMITS) == 0
            ):
                missing_fields.append("GLOBAL_CHAT_RATE_LIMITS")

            if missing_fields:
                raise ValueError(
                    f"When RATE_LIMIT_ENABLED is True, the following fields are required: {', '.join(missing_fields)}"
                )

        return self


settings = Settings()
