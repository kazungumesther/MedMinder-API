from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class ReminderBase(BaseModel):
    medication_id: UUID
    reminder_time: str = Field(..., description="Time format in HH:MM")
    is_active: bool = True

class ReminderCreate(ReminderBase):
    pass

class ReminderResponse(ReminderBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
