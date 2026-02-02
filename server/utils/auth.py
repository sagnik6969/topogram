from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException, status, Request
from firebase_admin import auth

security = HTTPBearer(auto_error=False)


def authenticate_user(request: Request, token=Depends(security)) -> bool:
    if(request.url.path == '/main_backend_service/health'):
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
        print(token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": f"Invalid authorization token: {e}",
                "status": "Unauthorized",
            },
        )
