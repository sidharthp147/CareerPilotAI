from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from database import Base
class Users(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    email=Column(String(25))
    password_hash=Column(String(100))
    role=Column(String(20))
    is_active=Boolean
    created_at=Column(DateTime)
class JobSeekers(Base):
    __tablename__="jobseekers"
    user_id=Column(Integer,ForeignKey('users.id'),primary_key=True)
    name=Column(String(50))
    skills=Column(String(100))
    experience=Column(Float)
    resume_url=Column(String(100))
class Recruiters(Base):
    __tablename__="recruiters"
    user_id=Column(Integer,ForeignKey('users.id'),primary_key=True)
    company_name=Column(String(50))
    company_description=Column(String(100))
    is_approved=Column(Boolean)
class Jobs(Base):
    __tablename__="jobs"
    id=Column(Integer,primary_key=True)
    recruiter_id=Column(Integer,ForeignKey('recruiters.user_id'))
    heading=Column(String(100))
    skills=Column(String(100))
    description=Column(String(100))
    location=Column(String(100))
    salary_range=Column(String(100))
    job_type=Column(String(100))
    created_at=Column(DateTime)
class Applications(Base):
    __tablename__="applications"
    id=Column(Integer,primary_key=True)
    job_id=Column(Integer,ForeignKey('jobs.id'))
    job_seeker_id=Column(Integer,ForeignKey('jobseekers.user_id'))
    status=Column(String(100))
    applied_at=Column(DateTime)

class RefreshToken(Base):
    __tablename__="refreshtokens"
    id=Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token_hash = Column(String(100), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)