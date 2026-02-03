diagram-copilot/
├── server/
│ ├── app/
│ │ ├── **init**.py
│ │ ├── main.py # FastAPI app creation
│ │ ├── config/
│ │ │ ├── **init**.py
│ │ │ └── settings.py # Settings with Pydantic
│ │ ├── api/
│ │ │ ├── **init**.py
│ │ │ ├── v1/
│ │ │ │ ├── **init**.py
│ │ │ │ └── endpoints/
│ │ │ │ ├── **init**.py
│ │ │ │ └── diagrams.py
│ │ │ └── deps.py # Dependencies
│ │ ├── services/
│ │ │ ├── **init**.py
│ │ │ └── diagram_service.py
│ │ ├── models/
│ │ │ ├── **init**.py
│ │ │ └── diagram.py # Pydantic models
│ │ ├── schemas/
│ │ │ ├── **init**.py
│ │ │ └── diagram.py # Request/response schemas
│ │ └── utils/
│ │ ├── **init**.py
│ │ └── logger.py
│ ├── tests/
│ │ ├── **init**.py
│ │ ├── conftest.py
│ │ └── test_api.py
│ ├── .env # Local development (git-ignored)
│ ├── .env.example # Template
│ ├── pyproject.toml
│ ├── run.py # Entry point (instead of main.py)
│ └── README.md

# Build and push the Docker image to ECR
