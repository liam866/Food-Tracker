from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.relational.database import get_db
from app.schemas.internal import UserProfileUpdate
from app.services.user_service import get_user_profile, set_user_profile, delete_user_profile

router = APIRouter()

@router.get("/user/profile")
async def get_user_profile_endpoint(db: Session = Depends(get_db)):
    return get_user_profile(db)

@router.post("/user/profile")
async def set_user_profile_endpoint(profile: UserProfileUpdate, db: Session = Depends(get_db)):
    return set_user_profile(profile, db)

@router.delete("/user/profile")
async def delete_user_profile_endpoint(db: Session = Depends(get_db)):
    return delete_user_profile(db)
