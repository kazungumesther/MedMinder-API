from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Literal

class AdherenceLogBase(BaseModel):
    reminder_id: UUID
    status: Literal["TAKEN", "SKIPPED", "MISSED"] = Field(..., description="Current status of the dose")

class AdherenceLogCreate(AdherenceLogBase):
    pass

class AdherenceLogResponse(AdherenceLogBase):
    id: UUID
    logged_at: datetime

    class Config:
        from_attributes = True
