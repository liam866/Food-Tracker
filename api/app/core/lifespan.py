from fastapi import FastAPI

async def lifespan_handler(app: FastAPI):
    # API container no longer manages database state
    pass
