# Topogram

Topogram is an open-source, AI-powered diagramming tool designed as a free alternative to Eraser.io. It leverages the power of Large Language Models (LLMs) to generate and edit diagrams effortlessly, streamlining documentation and architectural design for developers.

Built with a focus on simplicity, Topogram allows you to transform text descriptions into clear, editable visual diagrams instantly.

## 🚀 Key Features

- **🤖 AI Generation**: Create complex architecture diagrams instantly from simple text descriptions using advanced AI models.
- **✏️ Visual Editing**: Refine and update your diagrams with an intuitive drag-and-drop interface.
- **☁️ Icon Support**: Native support for **AWS** service icons helps you visualize cloud architectures effectively.
- **🔄 Seamless Updates**: Easily modify generated diagrams through direct manipulation or follow-up prompts.

## 🗺️ Future Roadmap

We are actively working on expanding Topogram's capabilities:

- [ ] **Multi-Cloud Support**: Integration for **Google Cloud Platform (GCP)** and **Microsoft Azure** icons.
- [ ] **General-Purpose Icons**: A comprehensive library of standard icons for diverse use cases.
- [ ] **Collaborative Editing**: Real-time multiplayer editing capabilities.

## 🛠️ Tech Stack

Topogram is built using modern, scalable technologies:

- **Frontend**: React, Vite, Excalidraw
- **Backend API**: Python (FastAPI), managed with `uv`
- **AI Integration**: LangChain, ChatCerebras (gpt-oss)
- **Monitoring**: LangFuse (for LLM observability)
- **Database**: Firestore (Emulated locally for development), Redis
- **Rendering**: Node.js microservice for diagram layout (ELK)

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Docker**: [Install Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Docker Compose**: Included with Docker Desktop.
- **Git**: [Install Git](https://git-scm.com/downloads)

## 📦 Installation & Setup

Follow these steps to get Topogram up and running locally:

### 1. Clone the Repository

```bash
git clone https://github.com/sagnik6969/topogram.git
cd topogram
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory based on the provided example:

```bash
cp .env.example .env
```

Open the `.env` file and configure the following variables.

#### Required Environment Variable

| Variable                  | Description                                                                                                                  | Example                         |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| `DEFAULT_CHAT_MODEL_NAME` | The LLM model to use for diagram generation. Format follows LangChain's `init_chat_model` convention: `provider:model_name`. | `google_genai:gemini-2.0-flash` |

#### Model-Specific Environment Variables

Set the API key for the provider you chose in `DEFAULT_CHAT_MODEL_NAME`. You only need to set the key for the provider you are using.

| Provider          | `DEFAULT_CHAT_MODEL_NAME` Example    | Required Env Variable                                                 | Get API Key                                             |
| ----------------- | ------------------------------------ | --------------------------------------------------------------------- | ------------------------------------------------------- |
| **Google Gemini** | `google_genai:gemini-2.0-flash`      | `GOOGLE_API_KEY`                                                      | [Google AI Studio](https://aistudio.google.com/apikey)  |
| **OpenAI**        | `openai:gpt-4o`                      | `OPENAI_API_KEY`                                                      | [OpenAI Platform](https://platform.openai.com/api-keys) |
| **Azure OpenAI**  | `azure_openai:gpt-4o`                | `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `OPENAI_API_VERSION` | [Azure Portal](https://portal.azure.com/)               |
| **Anthropic**     | `anthropic:claude-sonnet-4-20250514` | `ANTHROPIC_API_KEY`                                                   | [Anthropic Console](https://console.anthropic.com/)     |
| **Groq**          | `groq:llama-3.3-70b-versatile`       | `GROQ_API_KEY`                                                        | [Groq Console](https://console.groq.com/keys)           |
| **Cerebras**      | `cerebras:llama-3.3-70b`             | `CEREBRAS_API_KEY`                                                    | [Cerebras Cloud](https://cloud.cerebras.ai/)            |

**Example `.env` configuration (using Google Gemini):**

```env
DEFAULT_CHAT_MODEL_NAME=google_genai:gemini-2.0-flash
GOOGLE_API_KEY=your_google_api_key_here
MAX_NUMBER_OF_CHARACTERS_IN_CHAT_MESSAGE=2000
```

> **Note**: The model name format follows LangChain's [`init_chat_model`](https://python.langchain.com/docs/how_to/chat_models_universal_init/) convention. The provider prefix (e.g., `google_genai:`, `openai:`) tells LangChain which integration to use. Cerebras models use a special `cerebras:` prefix and are handled via the `ChatCerebras` class directly.

### 3. Run with Docker Compose

Build and start the application services:

```bash
docker-compose up --build
```

This command will start the following services:

- **Client**: Frontend application (React)
- **Server**: Backend API (FastAPI)
- **Rendering Engine**: Diagram layout service
- **Firestore Emulator**: Local database

### 4. Access the Application

Once the containers are up and running, access the application in your browser:

- **Frontend**: [http://localhost:9753](http://localhost:9753)
- **Backend API Docs**: [http://localhost:9754/docs](http://localhost:9754/docs)

## 🤝 Contributing

Contributions are welcome! If you'd like to improve Topogram, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Commit your changes (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/YourFeature`).
5.  Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by [Sagnik Jana](https://github.com/sagnik6969)
