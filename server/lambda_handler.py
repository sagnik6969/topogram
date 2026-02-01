"""
AWS Lambda handler for FastAPI application using Mangum
"""

from mangum import Mangum
from app.main import app

# Create the Lambda handler by wrapping the FastAPI app with Mangum
handler = Mangum(app, lifespan="off")
