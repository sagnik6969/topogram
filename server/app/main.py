import logging
from fastapi import FastAPI, Depends
from app.api.v1 import router as v1_router
from app.config.settings import settings
from contextlib import asynccontextmanager
from firebase_admin import initialize_app, delete_app
from utils.auth import authenticate_user, authentication_middleware
from fastapi.middleware.cors import CORSMiddleware
from langfuse import get_client
import redis
from fastapi import HTTPException
from app.core.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIASGIMiddleware
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
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# IMPORTANT: Middleware execution order is REVERSE of how they're added
# So we add them in reverse order of desired execution
# Desired order: Auth -> RateLimit -> CORS

app.add_middleware(SlowAPIASGIMiddleware)

# Use FastAPI's middleware decorator for authentication
@app.middleware("http")
async def auth_middleware(request, call_next):
    return await authentication_middleware(request, call_next)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORES_ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(v1_router)


@app.get("/health")
@limiter.exempt
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
