import logging
from fastapi import FastAPI, Depends
from app.api.v1 import router as v1_router
from app.config.settings import settings
from contextlib import asynccontextmanager
from firebase_admin import initialize_app, delete_app
from utils.auth import authenticate_user
from fastapi.middleware.cors import CORSMiddleware
from langfuse import get_client
import redis
from fastapi import HTTPException
from app.core.rate_limit import limiter, get_user_id
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
if settings.DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.ERROR)


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP LOGIC ---
    firebase_app = initialize_app()
    _ = get_client()

    yield  # The application runs here

    # --- SHUTDOWN LOGIC ---
    # Shutdown Firebase
    try:
        delete_app(firebase_app)
        logger.info("Shutdown: Firebase app deleted.")
    except Exception as e:
        logger.warning(f"Shutdown: Firebase app cleanup failed: {e}")


app = FastAPI(
    root_path="/main_backend_service",
    lifespan=lifespan,
    dependencies=[
        Depends(authenticate_user),
        # Global DDoS Protection: 100 requests per minute per IP
        Depends(limiter.limit("100/minute")),
        # Per-User Rate Limit: 1000 requests per hour per user
        Depends(limiter.limit("1000/hour", key_func=get_user_id)),
    ],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORES_ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)


@app.get("/health")
async def health_check():
    try:
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD.get_secret_value(), socket_connect_timeout=3,retry_on_timeout=True)
        if r.ping():
            return {"status": "success", "message": f"Connected to Redis at {settings.REDIS_HOST}"}
    except redis.ConnectionError as e:
        raise HTTPException(status_code=500, detail=f"Redis connection failed: {str(e)}")
        logger.exception(e)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
