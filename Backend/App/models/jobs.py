from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, UniqueConstraint
from core.database import Base
class Jobs(Base):
    __tablename__="jobs"
    id=Column(Integer,primary_key=True)
    recruiter_id=Column(Integer,ForeignKey('recruiters.user_id'))
    heading=Column(String(100))
    skills=Column(String(1000))
    description=Column(String(5000))
    location=Column(String(100))
    salary_range=Column(String(100))
    experience=Column(String(100))
    job_type=Column(String(100))
    created_at=Column(DateTime)
    is_deleted=Column(Boolean,default=False)
    deleted_at=Column(DateTime,nullable=True)
    def to_dict(self):
        return {
        "id": self.id,
        "recruiter_id": self.recruiter_id,
        "heading": self.heading,
        "skills": self.skills,
        "description": self.description,
        "location": self.location,
        "salary_range": self.salary_range,
        "experience": self.experience,
        "job_type": self.job_type,
        "created_at": self.created_at.isoformat() if self.created_at else None,
        "is_deleted": self.is_deleted,
        "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
    }
class Skills(Base):
    __tablename__="skills"
    id=Column(Integer,primary_key=True)
    skill=Column(String(100),unique=True) 
class JobSkills(Base):
    __tablename__="job_skills"
    id=Column(Integer,primary_key=True)
    job_id=Column(Integer,ForeignKey('jobs.id'))
    skill_id=Column(Integer,ForeignKey('skills.id'))
    __table_args__ = (UniqueConstraint('job_id', 'skill_id', name='unique_job_skill'),) 
class SavedJobs(Base):
    __tablename__="saved_jobs"
    id=Column(Integer,primary_key=True)
    job_id=Column(Integer,ForeignKey('jobs.id'))
    job_seeker_id=Column(Integer,ForeignKey('jobseekers.user_id'))
    __table_args__ = (UniqueConstraint('job_id', 'job_seeker_id', name='unique_job_user_saved'),)
