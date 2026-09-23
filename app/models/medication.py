import uuid
from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Medication(Base):
    __tablename__ = "medications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    
    user_id = Column(UUID(as_uuid=True), nullable=False)
    
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    stock_quantity = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    reminders = relationship("Reminder", back_populates="medication", cascade="all, delete-orphan")
