# Nutrition Tracker

Nutrition Tracker is a containerized food‑tracking application that combines OCR‑based menu parsing with Retrieval‑Augmented Generation (RAG) to produce grounded, explainable dietary recommendations. The system is implemented as a modular microservices architecture with clearly separated responsibilities and a fully traceable end‑to‑end data flow.

---

## Key Features

### Menu Analysis (OCR + RAG)

Users can upload a photo of a restaurant menu and receive structured menu items along with goal‑aware dietary recommendations.

**Image Processing (Vision Service)**

*   Image preprocessing
*   Layout detection to segment menu regions
*   OCR to extract text from each region

**Retrieval‑Augmented Generation**

*   Semantic search using Qdrant
*   Extracted menu items are embedded and matched against a vector database of known foods
*   A similarity threshold ensures only high‑confidence matches are used
*   Relevant foods and their nutritional data are retrieved and passed to the LLM as context

**LLM‑Based Recommendations**

*   A local LLM (via Ollama) generates:

    *   Top 3 menu recommendations
    *   Goal‑aware suggestions based on remaining calories and protein
*   The model is strictly constrained to retrieved nutritional context (no free hallucination)

**Explainability**

*   Each recommendation includes the nutritional data and reasoning used to reach the decision

---

### Food Logging

Core food‑tracking functionality operates independently of AI features.

*   Manual food logging with gram‑based quantities
*   Automatic calculation of calories and macronutrients
*   Full CRUD support for food log entries
*   Daily summaries compared against user‑defined targets

---

## Architecture Overview

The system consists of isolated services communicating over HTTP, each responsible for a single concern.

### High‑Level Flow

*   The frontend communicates exclusively with the API service
*   Images are forwarded to the Vision service for OCR
*   Extracted menu items are sent to the Vector service for semantic matching
*   Nutritional data is retrieved from the Relational service
*   The LLM (via Ollama) generates grounded recommendations
*   Results are aggregated by the API and returned to the client

---

## Services

### `api` — API Gateway

*   Request validation and orchestration
*   Coordinates internal service calls and LLM interactions
*   Technology: FastAPI

### `relational` — Relational Data Service (SQLite)

*   Authoritative storage for:

    *   Food catalog
    *   Food logs
    *   User goals
*   Provides structured nutritional data
*   Integrates with the Vector service for semantic lookup and seeding
*   Technologies: FastAPI, SQLAlchemy, Pandas, httpx

### `vector` — Semantic Search Service

*   Manages embeddings and similarity search
*   Interfaces with Qdrant
*   Generates embeddings via Ollama
*   Seeds data only when required on startup
*   Technologies: FastAPI, Qdrant Client, httpx

### `vision` — OCR Service

*   Image preprocessing
*   Layout detection
*   Image‑to‑text extraction
*   Technologies: FastAPI, PaddleOCR, OpenCV

### External Services

*   **Qdrant** — Vector database for food embeddings
*   **Ollama** — Local LLM and embedding provider

---

## Running Locally

### Prerequisites

*   **Docker** — Ensure Docker is installed and running
*   **Ollama** — Install locally and pull the required models:

    ```bash
    ollama pull qwen2.5:0.5b
    ollama pull all-minilm
    ```

    The `api` service uses `qwen2.5:0.5b` for text generation

    `all-minilm` is used for embeddings

---

### Environment Configuration

Create a `.env` file in the project root (next to `docker-compose.yml`) with the following values:

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

**Note**: `OLLAMA_BASE_URL` is set to `http://host.docker.internal:11434` to allow Docker Compose services to access Ollama running on the host machine. Adjust this if Ollama is running elsewhere (for example, inside another container).

---

### Start Services

From the project root directory:

```bash
docker compose up --build
```

---

### Access

Once all services are running (initial startup may take a few moments due to data seeding), open your browser and navigate to:

```
http://localhost:8000
```

---

## Possible Extensions

*   Authentication and multi‑user support
*   Long‑term dietary analytics and trend visualization
*   Conversational meal planning
*   Faster, real‑time food logging workflows
