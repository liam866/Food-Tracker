from pydantic import BaseModel
import enum

class SexEnum(str, enum.Enum):
    male = "male"
    female = "female"

class GoalEnum(str, enum.Enum):
    lose_fat = "lose_fat"
    maintain = "maintain"
    build_muscle = "build_muscle"

class UserProfileBase(BaseModel):
    name: str
    height_cm: float
    weight_kg: float
    age: int
    sex: SexEnum
    goal: GoalEnum

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileSchema(UserProfileBase):
    id: int = 1
    calorie_target: float
    protein_target: float

    class Config:
        orm_mode = True
