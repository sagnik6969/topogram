from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request
from app.config.settings import settings


def get_user_id(request: Request) -> str:
    """
    Extracts the user ID from the request state.
    This assumes that the `authenticate_user` dependency has already run
    and populated `request.state.uid`.
    If no user ID is found (e.g., public endpoint), it falls back to IP.
    """
    if hasattr(request.state, "uid"):
        return str(request.state.uid)
    return get_remote_address(request)


# Initialize the Limiter
# storage_uri is constructed from settings. 
# slowapi expects `redis://` or `rediss://`
# If your redis password has special chars, it might need encoding, but usually this is fine.
redis_url = f"redis://:{settings.REDIS_PASSWORD.get_secret_value()}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

limiter = Limiter(
    key_func=get_remote_address, # Default to IP-based if not specified
    storage_uri=redis_url,
    strategy="fixed-window", # Simple fixed window strategy
    enabled=settings.RATE_LIMIT_ENABLED,
)
