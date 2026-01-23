from fastapi import FastAPI, Depends
from app.api.v1 import router as v1_router
import logging
from app.config.settings import settings
from contextlib import asynccontextmanager
from firebase_admin import initialize_app, delete_app
from utils.auth import authenticate_user
from fastapi.middleware.cors import CORSMiddleware

if settings.DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.ERROR)


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP LOGIC ---
    firebase_app = initialize_app()
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
    dependencies=[Depends(authenticate_user)],
)

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
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
