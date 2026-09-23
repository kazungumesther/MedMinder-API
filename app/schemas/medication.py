from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class MedicationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    dosage: str = Field(..., description="e.g., '200mg' or '2 drops'")
    stock_quantity: int = Field(default=0, ge=0, description="Stock cannot be negative")

class MedicationCreate(MedicationBase):
    pass

class MedicationResponse(MedicationBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
