from fastapi import FastAPI
from app.api.v1 import router as v1_router
import logging
from app.config.settings import settings
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.db.models import UserThread

if settings.DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.ERROR)


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP LOGIC ---
    # Create the Motor client
    client = AsyncIOMotorClient(settings.MONGODB_URI.get_secret_value())

    # Initialize Beanie with the default database from the URI
    await init_beanie(
        database=client.get_default_database(), document_models=[UserThread]
    )
    logger.info("Startup: Beanie initialized.")

    yield  # The application runs here

    # --- SHUTDOWN LOGIC ---
    # Close the connection when the app stops
    client.close()
    logger.info("Shutdown: Database connection closed.")


app = FastAPI(root_path="/main_backend_service", lifespan=lifespan)

app.include_router(v1_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
