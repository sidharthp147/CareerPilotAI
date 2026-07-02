from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, UniqueConstraint
from core.database import Base
class Users(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    email=Column(String(25),unique=True,index=True)
    password_hash=Column(String(100))
    role=Column(String(20))
    is_active=Column(Boolean)
    created_at=Column(DateTime)
    is_verified=Column(Boolean)
    verification_token=Column(String(100))
    token_expiry=Column(DateTime)
class JobSeekers(Base):
    __tablename__="jobseekers"
    user_id=Column(Integer,ForeignKey('users.id'),primary_key=True)
    name=Column(String(50))
    skills=Column(String(100))
    experience=Column(Float)
    resume_url=Column(String(500))
    resume_status=Column(String(50))
class UserSkills(Base):
    __tablename__="user_skills"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey('jobseekers.user_id'))
    skill_id=Column(Integer,ForeignKey('skills.id'))
    __table_args__ = (UniqueConstraint('user_id', 'skill_id', name='unique_user_skill'),)  
class ResumeData(Base):
    __tablename__="resume_data"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey('jobseekers.user_id'))
    full_name=Column(String(50))
    role=Column(String(100))
    email=Column(String(50))
    phone=Column(String(20))
    skills=Column(String(500))
    experience=Column(String(2000))
    education=Column(String(500))
    projects=Column(String(1000))
    certifications=Column(String(500))
    linkedin=Column(String(100))
    github=Column(String(100))
    summary=Column(String(1000))
class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(String(500), nullable=False)
    type = Column(String(50), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime)
 