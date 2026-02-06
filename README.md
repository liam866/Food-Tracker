# Food Tracker 

Food Tracker is a containerized food tracking application with OCR-based menu parsing and AI-assisted recommendations via RAG. It is built as a modular microservices system with clearly separated responsibilities and grounded data flow.

## Key Features

### Menu Analysis (OCR + RAG)

Users can upload a photo of a menu and receive structured menu items and dietary recommendations.

*   **Image Processing** (vision)
    *   Layout detection to segment menu text regions
    *   OCR to extract machine-readable text

*   **Retrieval-Augmented Generation**
    *   Semantic Search (Qdrant): Menu items are embedded and matched against a vector database of known foods
    *   Nutritional Lookup (SQLite): Calories and macronutrients are retrieved from the relational database

*   **LLM-Based Recommendations**
    *   A local LLM (via Ollama) generates:
        *   Top 3 menu recommendations
        *   Goal-aware suggestions based on remaining calories and protein
    *   The model is constrained to retrieved nutritional context only

*   **Explainability**
    *   Recommendations include the nutritional data used in the decision

### Food Logging

Core food tracking works independently of AI features.

*   Manual food logging with gram-based quantities
*   Automatic calculation of calories and macronutrients
*   Full CRUD support for food log entries
*   Daily summary view against user-defined targets

## Architecture Overview

The system consists of isolated services communicating over HTTP, each focused on a single concern.

### High-Level Flow

*   The frontend interacts only with the API service
*   Images are forwarded to the Vision service for OCR
*   Extracted menu items are sent to the Vector service for semantic matching
*   Nutritional data is retrieved from the Relational service
*   The LLM (via Ollama) generates grounded recommendations
*   Results are aggregated and returned to the client

### Services

*   **`api` — API Gateway**
    *   Request validation and orchestration
    *   Coordinates internal services and LLM calls
    *   Technology: FastAPI

*   **`relational` — Relational Data Service (SQLite)**
    *   Authoritative storage for:
        *   Food catalog
        *   Food logs
        *   User goals
    *   Provides structured nutritional data
    *   Integrates with the Vector service for semantic lookup and seeding
    *   Technologies: FastAPI, SQLAlchemy, Pandas, httpx

*   **`vector` — Semantic Search Service (Qdrant)**
    *   Manages embeddings and similarity search
    *   Interfaces with Qdrant
    *   Generates embeddings via Ollama
    *   Seeds data only when required on startup
    *   Technologies: FastAPI, Qdrant Client, httpx

*   **`vision` — OCR Service**
    *   Image-to-text extraction
    *   Layout detection and OCR
    *   Technologies: FastAPI, PaddleOCR

*   **External Services**
    *   **Qdrant**: Vector database for food embeddings
    *   **Ollama**: Local LLM and embedding provider

## Running Locally

### Prerequisites

*   **Docker**: Ensure Docker is installed and running.
*   **Ollama**: Install [Ollama](https://ollama.ai/) locally and pull the required models:

    ```bash
    ollama pull qwen2.5:0.5b
    ollama pull all-minilm
    ```

    (The `api` service uses `qwen2.5:0.5b` for chat, and the `vector` service uses `all-minilm` for embeddings.)

### Environment Configuration

*   Create a `.env` file in the project root (next to `docker-compose.yml`) with the following values:

    ```env
    RELATIONAL_SERVICE_URL=http://relational:8000
    VECTOR_SERVICE_URL=http://vector:8000
    VISION_SERVICE_URL=http://vision:8000
    DATABASE_URL=sqlite:///./data/foodtracker.db
    QDRANT_URL=http://qdrant:6333
    OLLAMA_BASE_URL=http://host.docker.internal:11434
    CHAT_MODEL=qwen2.5:0.5b
    EMBED_MODEL=all-minilm
    ```

    **Note**: `OLLAMA_BASE_URL` is set to `http://host.docker.internal:11434` for Docker Compose to access Ollama running directly on your host machine. Adjust this if Ollama is running elsewhere (e.g., in another Docker container).

### Start Services

From the project root directory, run:

```bash
docker compose up --build
```

### Access

Once all services are running (this may take a few moments, especially during initial data seeding), open your web browser and navigate to:

`http://localhost:8000`

## Possible Extensions

*   Authentication and multi-user support
*   Long-term dietary analytics and trend visualization
*   Conversational meal planning
*   Faster, real-time logging workflows
