from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.database import get_db
from app.schemas.adherence import AdherenceLogCreate, AdherenceLogResponse
from app.services.adherence import AdherenceService

router = APIRouter(prefix="/adherence", tags=["Adherence Logs"])

@router.post("", response_model=AdherenceLogResponse, status_code=status.HTTP_201_CREATED)
def record_dose_status(payload: AdherenceLogCreate, db: Session = Depends(get_db)):
    service = AdherenceService(db)
    return service.log_adherence(payload)

@router.get("/reminder/{reminder_id}", response_model=List[AdherenceLogResponse])
def get_reminder_history(reminder_id: UUID, db: Session = Depends(get_db)):
    service = AdherenceService(db)
    return service.fetch_history(reminder_id)
