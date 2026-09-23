from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status
from app.repositories.medication import MedicationRepository
from app.schemas.medication import MedicationCreate

class MedicationService:
    def __init__(self, db: Session):
        self.repository = MedicationRepository(db)

    def add_medication(self, med_data: MedicationCreate):
        return self.repository.create(med_data)

    def get_medication_by_id(self, med_id: UUID):
        med = self.repository.get_by_id(med_id)
        if not med:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Medication record not found"
            )
        return med

    def list_all_medications(self):
        return self.repository.get_all()
