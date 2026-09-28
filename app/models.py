from sqlalchemy import Column, Integer, String, Text
from .database import Base


class UserPlan(Base):
    __tablename__ = "user_plans"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    user_id = Column(String(100), nullable=False)

    age = Column(Integer, nullable=False)

    weight = Column(String(50), nullable=True)

    goal = Column(String(100), nullable=False)

    intensity = Column(String(50), nullable=False)

    workout_plan = Column(Text, nullable=False)

    nutrition_tip = Column(Text, nullable=False)