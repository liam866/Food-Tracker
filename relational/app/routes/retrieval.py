from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.relational.database import get_db
from app.schemas.internal import RetrievalRequest
from app.services.retrieval_service import retrieve_context

router = APIRouter()

@router.post("/retrieve-context")
async def retrieve_context_endpoint(request: RetrievalRequest, db: Session = Depends(get_db)):
    return await retrieve_context(request.menu_items)
