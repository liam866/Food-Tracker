import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.core.lifespan import lifespan_handler
from app.routes import foods, logs, user, chat
from app.services.ollama_client import OllamaClient # Import OllamaClient
from app.core.config import settings # Import settings
from app.schemas.ollama import OllamaGenerateRequest # Import for health check

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup.")
    # Initialize OllamaClient during lifespan
    app.state.ollama_client = OllamaClient(base_url=settings.OLLAMA_BASE_URL)
    await lifespan_handler(app)
    yield
    logger.info("Application shutdown.")
    # Close OllamaClient during shutdown
    await app.state.ollama_client.client.aclose()
    logger.info("[Main] Ollama HTTPX client closed during shutdown.")

app = FastAPI(lifespan=lifespan)

# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Response: {response.status_code} (took {duration:.2f}s)")
    return response

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="./app/static"), name="static")

app.include_router(foods.router)
app.include_router(logs.router)
app.include_router(user.router)
app.include_router(chat.router)

@app.get("/health")
async def health_check():
    logger.info("[HealthCheck] Running LLM connectivity test...")

    try:
        ollama_client: OllamaClient = app.state.ollama_client

        test_request = OllamaGenerateRequest(
            prompt="Testing..",
            model=settings.OLLAMA_MODEL,
        )

        ollama_response = await ollama_client.generate(test_request)

        if ollama_response.response:
            logger.info("[HealthCheck] LLM responded successfully.")
            return {
                "status": "ok",
                "llm_status": "connected"
            }

        logger.warning("[HealthCheck] LLM responded but response was empty.")
        return {
            "status": "ok",
            "llm_status": "connected_but_empty"
        }

    except Exception as e:
        logger.error(f"[HealthCheck] LLM connection failed: {e}")
        return {
            "status": "ok",
            "llm_status": "disconnected",
            "error": str(e)
        }


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("app/static/index.html") as f:
        return HTMLResponse(content=f.read())
