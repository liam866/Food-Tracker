import logging
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.db.models import UserProfile
from app.services.calorie_calc import calculate_calorie_target, calculate_protein_target
from app.schemas.user import UserProfileCreate, UserProfileSchema

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/user/profile", response_model=UserProfileSchema)
async def set_user_profile(profile: UserProfileCreate, db: Session = Depends(get_db)):
    calorie_target = calculate_calorie_target(
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        age=profile.age,
        sex=profile.sex,
        goal=profile.goal,
    )
    protein_target = calculate_protein_target(weight_kg=profile.weight_kg)

    user_profile = db.query(UserProfile).filter(UserProfile.id == 1).first()
    if user_profile:
        logger.info(f"Updating existing user profile for ID 1.")
        user_profile.name = profile.name
        user_profile.height_cm = profile.height_cm
        user_profile.weight_kg = profile.weight_kg
        user_profile.age = profile.age
        user_profile.sex = profile.sex
        user_profile.goal = profile.goal
        user_profile.calorie_target = calorie_target
        user_profile.protein_target = protein_target
    else:
        logger.info(f"Creating new user profile with ID 1.")
        user_profile = UserProfile(
            id=1,
            name=profile.name,
            height_cm=profile.height_cm,
            weight_kg=profile.weight_kg,
            age=profile.age,
            sex=profile.sex,
            goal=profile.goal,
            calorie_target=calorie_target,
            protein_target=protein_target,
        )
        db.add(user_profile)

    db.commit()
    db.refresh(user_profile)
    logger.info(f"User profile for ID 1 successfully saved.")
    return user_profile


@router.get("/user/profile", response_model=Optional[UserProfileSchema])
async def get_user_profile(db: Session = Depends(get_db)):
    logger.info("Attempting to fetch user profile for ID 1.")
    user_profile = db.query(UserProfile).filter(UserProfile.id == 1).first()
    if user_profile:
        logger.info("User profile found for ID 1.")
    else:
        logger.warning("No user profile found for ID 1.")
    return user_profile

@router.delete("/user/profile", status_code=204)
async def delete_user_profile(db: Session = Depends(get_db)):
    logger.info("Attempting to delete user profile for ID 1.")
    user_profile = db.query(UserProfile).filter(UserProfile.id == 1).first()
    if not user_profile:
        logger.error("Failed to delete profile: User profile with ID 1 not found.")
        raise HTTPException(status_code=404, detail="User profile not found")
    
    db.delete(user_profile)
    db.commit()
    logger.info("User profile for ID 1 successfully deleted.")
    return Response(status_code=204)
