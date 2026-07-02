from sqlalchemy import Column, Enum, Integer, String, Boolean, DateTime, ForeignKey, Float, UniqueConstraint
from core.database import Base
import enum
class ApplicationStatus(str,enum.Enum):
    APPLIED="APPLIED"
    REJECTED="REJECTED"
    ACCEPTED="ACCEPTED"
class Applications(Base):
    __tablename__="applications"
    id=Column(Integer,primary_key=True)
    job_id=Column(Integer,ForeignKey('jobs.id'))
    job_seeker_id=Column(Integer,ForeignKey('jobseekers.user_id'))
    status=Column(Enum(ApplicationStatus))
    applied_at=Column(DateTime)
    __table_args__ = (
        UniqueConstraint('job_id', 'job_seeker_id', name='uq_job_user_application'),)