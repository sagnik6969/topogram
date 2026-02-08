from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException, status, Request
from firebase_admin import auth
from starlette.responses import JSONResponse
from app.config.settings import settings

security = HTTPBearer(auto_error=False)


async def authentication_middleware(request: Request, call_next):
    """
    Middleware to authenticate users via Firebase token.
    This runs before rate limiting to ensure request.state.uid is available.
    """

    if settings.AUTH_DISABLED:
        # If authentication is disabled, set a default user ID and proceed
        request.state.uid = settings.USER_ID_WHEN_AUTH_DISABLED
        response = await call_next(request)
        return response

    # Skip authentication for health check endpoint
    if request.url.path == "/main_backend_service/health":
        response = await call_next(request)
        return response

    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "message": "Authorization token is missing",
                "status": "Unauthorized",
            },
        )

    token = auth_header.split("Bearer ")[1]

    try:
        decoded_token = auth.verify_id_token(token)
        request.state.uid = decoded_token["uid"]
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "message": f"Invalid authorization token: {str(e)}",
                "status": "Unauthorized",
            },
        )

    response = await call_next(request)
    return response


def authenticate_user(request: Request, token=Depends(security)) -> bool:
    """
    Legacy dependency-based authentication.
    Note: This is kept for backward compatibility but middleware is preferred.
    """
    if request.url.path == "/main_backend_service/health":
        return True
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Authorization token is missing",
                "status": "Unauthorized",
            },
        )
    try:
        decoded_token = auth.verify_id_token(token.credentials)
        request.state.uid = decoded_token["uid"]
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": f"Invalid authorization token: {e}",
                "status": "Unauthorized",
            },
        )
