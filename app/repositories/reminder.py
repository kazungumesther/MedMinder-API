from sqlalchemy.orm import Session
from uuid import UUID
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate

class ReminderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, reminder_data: ReminderCreate) -> Reminder:
        db_reminder = Reminder(
            medication_id=reminder_data.medication_id,
            reminder_time=reminder_data.reminder_time,
            is_active=reminder_data.is_active
        )
        self.db.add(db_reminder)
        self.db.commit()
        self.db.refresh(db_reminder)
        return db_reminder

    def get_by_id(self, reminder_id: UUID) -> Reminder:
        return self.db.query(Reminder).filter(Reminder.id == reminder_id).first()

    def get_all_active(self) -> list[Reminder]:
        return self.db.query(Reminder).filter(Reminder.is_active == True).all()
