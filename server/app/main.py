from fastapi import FastAPI, HTTPException
from app.api.v1 import router as v1_router
from app.exceptions.diagrams import MermaidConversionError

app = FastAPI(root_path="/main_backend_service")

app.include_router(v1_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.exception_handler(MermaidConversionError)
async def mermaid_conversion_error_handler(_, exc: MermaidConversionError):
    raise HTTPException(status_code=exc.status_code, detail=exc.message)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
