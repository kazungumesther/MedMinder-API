from sqlalchemy.orm import Session
from uuid import UUID
from app.models.adherence import AdherenceLog
from app.schemas.adherence import AdherenceLogCreate

class AdherenceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, log_data: AdherenceLogCreate) -> AdherenceLog:
        db_log = AdherenceLog(
            reminder_id=log_data.reminder_id,
            status=log_data.status
        )
        self.db.add(db_log)
        self.db.commit()
        self.db.refresh(db_log)
        return db_log

    def get_logs_by_reminder(self, reminder_id: UUID) -> list[AdherenceLog]:
        return self.db.query(AdherenceLog).filter(AdherenceLog.reminder_id == reminder_id).all()
