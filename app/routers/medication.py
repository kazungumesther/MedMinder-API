from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.schemas.medication import MedicationCreate, MedicationResponse
from app.services.medication import MedicationService


router = APIRouter(prefix="/medications", tags=["Medications"])

@router.post("", response_model=MedicationResponse, status_code=status.HTTP_201_CREATED)
def create_medication(payload: MedicationCreate, db: Session = Depends(get_db)):
    """
    Register a new medication track record under an active account.
    """
    service = MedicationService(db)
    return service.add_medication(payload)

@router.get("", response_model=List[MedicationResponse])
def get_all_medications(db: Session = Depends(get_db)):
    """
    Retrieve all medications registered across the system.
    """
    service = MedicationService(db)
    return service.list_all_medications()

@router.get("/{med_id}", response_model=MedicationResponse)
def get_single_medication(med_id: UUID, db: Session = Depends(get_db)):
    """
    Fetch details for a single medication using its unique UUID.
    """
    service = MedicationService(db)
    return service.get_medication_by_id(med_id)
