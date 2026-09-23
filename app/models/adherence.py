import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class AdherenceLog(Base):
    __tablename__ = "adherence_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reminder_id = Column(UUID(as_uuid=True), ForeignKey("reminders.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False) 
    logged_at = Column(DateTime(timezone=True), server_default=func.now())
