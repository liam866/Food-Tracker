import logging
from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Optional

from app.clients.relational_client import RelationalClient, get_relational_client
from app.services.food.calorie_calc import calculate_calorie_target, calculate_protein_target
from app.schemas.user import UserProfileCreate, UserProfileSchema

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/user/profile", response_model=UserProfileSchema)
async def set_user_profile(profile: UserProfileCreate, db_client: RelationalClient = Depends(get_relational_client)):
    logger.info(f"[Backend] set_user_profile: Input profile data: {profile}")
    calorie_target = calculate_calorie_target(
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        age=profile.age,
        sex=profile.sex,
        goal=profile.goal,
    )
    protein_target = calculate_protein_target(weight_kg=profile.weight_kg)
    logger.info(f"[Backend] set_user_profile: Calculated calorie_target: {calorie_target}, protein_target: {protein_target}")

    user_profile = db_client.set_user_profile(profile, calorie_target, protein_target)
    
    logger.info(f"User profile for ID 1 successfully saved.")
    return user_profile


@router.get("/user/profile", response_model=Optional[UserProfileSchema])
async def get_user_profile(db_client: RelationalClient = Depends(get_relational_client)):
    logger.info("Attempting to fetch user profile for ID 1.")
    user_profile = db_client.get_user_profile()
    if user_profile:
        logger.info("User profile found for ID 1.")
    else:
        logger.warning("No user profile found for ID 1.")
    return user_profile

@router.delete("/user/profile", status_code=204)
async def delete_user_profile(db_client: RelationalClient = Depends(get_relational_client)):
    logger.info("Attempting to delete user profile for ID 1.")
    success = db_client.delete_user_profile()
    if not success:
        logger.error("Failed to delete profile: User profile with ID 1 not found.")
        raise HTTPException(status_code=404, detail="User profile not found")
    
    logger.info("User profile for ID 1 successfully deleted.")
    return Response(status_code=204)
