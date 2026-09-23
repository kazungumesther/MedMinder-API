from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.reminder import ReminderCreate, ReminderResponse
from app.services.reminder import ReminderService
from typing import List

router = APIRouter(prefix="/reminders", tags=["Reminders"])

@router.post("", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
def create_new_reminder(reminder: ReminderCreate, db: Session = Depends(get_db)):
    service = ReminderService(db)
    return service.create_reminder(reminder)

@router.get("", response_model=List[ReminderResponse])
def get_active_reminders(db: Session = Depends(get_db)):
    service = ReminderService(db)
    return service.fetch_active_reminders()
