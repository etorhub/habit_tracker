from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class HabitBase(SQLModel):
    name: str = Field(index=True)
    is_good: bool = Field(
        default=True, description="Whether this is a good or bad habit"
    )
    goal_streak: Optional[int] = Field(
        default=None, description="Target streak for this habit"
    )
    user_id: str = Field(index=True)


class Habit(HabitBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    current_streak: int = Field(default=0)
    longest_streak: int = Field(default=0)


class HabitRead(HabitBase):
    id: int
    created_at: datetime
    current_streak: int
    longest_streak: int


class HabitCreate(HabitBase):
    pass


class HabitUpdate(SQLModel):
    name: Optional[str] = None
    is_good: Optional[bool] = None
    goal_streak: Optional[int] = None
