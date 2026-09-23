from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status

from app.repositories.adherence import AdherenceRepository
from app.models.reminder import Reminder
from app.models.medication import Medication
from app.schemas.adherence import AdherenceLogCreate

class AdherenceService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = AdherenceRepository(db)

    def log_adherence(self, log_data: AdherenceLogCreate):
        """
        Record a medication dose tracking state and dynamically deduct 
        inventory stock if the medication was taken.
        """
       
        reminder = self.db.query(Reminder).filter(Reminder.id == log_data.reminder_id).first()
        if not reminder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Target schedule reminder not found"
            )
        
      
        if log_data.status == "taken":
            medication = self.db.query(Medication).filter(Medication.id == reminder.medication_id).first()
            if medication:
                if medication.stock_quantity > 0:
                    medication.stock_quantity -= 1
                else:
                    
                    print(f" Warning: Stock for {medication.name} is already at zero.")
        
        return self.repository.create(log_data)

    def fetch_history(self, reminder_id: UUID):
        """
        Fetch compliance logs for a specific reminder timeline.
        """
        return self.repository.get_logs_by_reminder(reminder_id)
