from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request
from app.config.settings import settings
from fastapi import HTTPException, Depends


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
    key_func=get_remote_address, # Default to IP-based for default_limits
    storage_uri=redis_url,
    strategy="fixed-window",
    enabled=settings.RATE_LIMIT_ENABLED,
    default_limits=["1/minute"], # Global IP limit
)

# Custom dependency for per-user rate limiting
from limits import parse

async def check_user_rate_limit(request: Request):
    if not settings.RATE_LIMIT_ENABLED:
        return
        
    user_id = get_user_id(request)
    # Check if this is a real user (not IP fallback)
    # If the user is unauthenticated or it fell back to IP in get_user_id, we might want to skip 
    # OR enforce it.
    # get_user_id falls back to remote address if no uid.
    # The per-user limit is 1000/hour.
    
    limit_item = parse("1000/hour")
    
    # We use the 'user' namespace for this limit to avoid collision with IP limits if keys overlap
    # formatted key: "user:{id}"
    key = f"user:{user_id}"
    
    # limiter.limiter is the underlying limits.strategies.RateLimiter
    # hit returns True if allowed, False if blocked
    if not limiter.limiter.hit(limit_item, key):
        raise HTTPException(
            status_code=429,
            detail="User rate limit exceeded: 1000/hour"
        )
