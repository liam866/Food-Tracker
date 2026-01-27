from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class SexEnum(enum.Enum):
    male = "male"
    female = "female"

class GoalEnum(enum.Enum):
    lose_fat = "lose_fat"
    maintain = "maintain"
    build_muscle = "build_muscle"

class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    calories_per_100g = Column(Float)
    protein_per_100g = Column(Float)
    carbs_per_100g = Column(Float)
    fat_per_100g = Column(Float)

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True, default=1)
    name = Column(String)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    age = Column(Integer)
    sex = Column(SQLEnum(SexEnum), default=SexEnum.male)
    goal = Column(SQLEnum(GoalEnum), default=GoalEnum.maintain)
    calorie_target = Column(Float)
    protein_target = Column(Float)

class FoodLog(Base):
    __tablename__ = "food_logs"

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, index=True)
    grams = Column(Float)
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fat = Column(Float)
    datetime = Column(DateTime(timezone=True), server_default=func.now())
