from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, nullable=False)
    status = Column(String, default="PENDING", nullable=False)
    total = Column(Integer, default=0)
    successful = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    certificates = relationship(
        "Certificate",
        back_populates="job",
        cascade="all, delete-orphan"
    )


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("generation_jobs.id"), nullable=False)

    recipient_name = Column(String, nullable=False)
    recipient_email = Column(String, nullable=False)

    status = Column(String, default="PENDING", nullable=False)
    file_path = Column(String, nullable=True)
    error_message = Column(String, nullable=True)

    job = relationship(
        "GenerationJob",
        back_populates="certificates"
    )