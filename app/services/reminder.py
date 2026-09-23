from sqlalchemy.orm import Session
from app.repositories.reminder import ReminderRepository
from app.schemas.reminder import ReminderCreate
from fastapi import HTTPException, status

class ReminderService:
    def __init__(self, db: Session):
        self.repository = ReminderRepository(db)

    def create_reminder(self, reminder_data: ReminderCreate):
        
        return self.repository.create(reminder_data)

    def fetch_active_reminders(self):
        return self.repository.get_all_active()
