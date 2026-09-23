from sqlalchemy.orm import Session
from uuid import UUID
from app.models.medication import Medication
from app.schemas.medication import MedicationCreate

class MedicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, med_data: MedicationCreate) -> Medication:
        db_medication = Medication(
            name=med_data.name,
            dosage=med_data.dosage,
            stock_quantity=med_data.stock_quantity
        )
        self.db.add(db_medication)
        self.db.commit()
        self.db.refresh(db_medication)
        return db_medication

    def get_by_id(self, med_id: UUID) -> Medication:
        return self.db.query(Medication).filter(Medication.id == med_id).first()

    def get_all(self) -> list[Medication]:
        return self.db.query(Medication).all()
