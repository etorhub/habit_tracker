from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class HabitLogBase(SQLModel):
    habit_id: int = Field(foreign_key="habit.id", index=True)
    date: date = Field(index=True)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)


class HabitLog(HabitLogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class HabitLogRead(HabitLogBase):
    id: int
    created_at: datetime
    updated_at: datetime


class HabitLogCreate(HabitLogBase):
    pass


class HabitLogUpdate(SQLModel):
    completed: Optional[bool] = None
