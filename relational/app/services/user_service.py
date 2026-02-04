from sqlalchemy.orm import Session
from app.relational import models
from app.schemas.internal import UserProfileUpdate

def get_user_profile(db: Session):
    return db.query(models.UserProfile).first()

def set_user_profile(profile: UserProfileUpdate, db: Session):
    p = db.query(models.UserProfile).filter(models.UserProfile.id == 1).first()
    if p:
        p.name = profile.name
        p.height_cm = profile.height_cm
        p.weight_kg = profile.weight_kg
        p.age = profile.age
        p.sex = models.SexEnum(profile.sex)
        p.goal = models.GoalEnum(profile.goal)
        p.calorie_target = profile.calorie_target
        p.protein_target = profile.protein_target
    else:
        p = models.UserProfile(
            id=1,
            name=profile.name,
            height_cm=profile.height_cm,
            weight_kg=profile.weight_kg,
            age=profile.age,
            sex=models.SexEnum(profile.sex),
            goal=models.GoalEnum(profile.goal),
            calorie_target=profile.calorie_target,
            protein_target=profile.protein_target
        )
        db.add(p)
    db.commit()
    db.refresh(p)
    return p

def delete_user_profile(db: Session):
    p = db.query(models.UserProfile).filter(models.UserProfile.id == 1).first()
    if p:
        db.delete(p)
        db.commit()
        return {"success": True}
    return {"success": False}
