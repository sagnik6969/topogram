from fastapi import FastAPI
from app.api.v1 import router as v1_router
import logging
from app.config.settings import settings

if settings.DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.ERROR)

app = FastAPI(root_path="/main_backend_service")

app.include_router(v1_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
