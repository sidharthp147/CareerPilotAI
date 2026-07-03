from datetime import datetime, timezone
import json
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.jobs import Jobs
from models.application import Applications
from models.recruiters import Recruiters
from models.users import JobSeekers
from models.jobs import Skills,JobSkills,SavedJobs
import hashlib
async def list_jobs(ids: list, search: str | None, job_type: str | None,skills: list | None,salary_range: str | None,experience: str | None, location: str | None, limit: int, offset: int, db: Session):
    stmt = db.query(Jobs)
    if ids:
        stmt=stmt.filter(Jobs.id.in_(ids)) 
        stmt=stmt.filter(Jobs.is_deleted == False)
        if location:
            location=location.strip().lower()
            stmt=stmt.filter(Jobs.location == location)
        if job_type:
            job_type=job_type.strip().lower()
            stmt=stmt.filter(Jobs.job_type == job_type) 
        total = stmt.count()
        jobs = stmt.limit(limit).offset(offset).all()
        jobs_list = [job.to_dict() for job in jobs]
        response={"total": total, "jobs": jobs_list}
        return response
    search = " ".join(search.strip().lower().split()) if search else None
    if search:
        stmt = stmt.filter(
            or_(
                Jobs.heading.ilike(f"%{search}%"),
              
            )
        )
    if skills:
        stmt = stmt.filter(Jobs.skills.contains(skills))
    if salary_range:
        stmt = stmt.filter(Jobs.salary_range == salary_range)
    if experience:
        stmt = stmt.filter(Jobs.experience == experience)
    if job_type:
        stmt = stmt.filter(Jobs.job_type == job_type)
    if location:
        stmt = stmt.filter(Jobs.location == location)
    stmt=stmt.filter(Jobs.is_deleted == False)
    total = stmt.count()
    jobs = stmt.limit(limit).offset(offset).all()
    jobs_list = [job.to_dict() for job in jobs]
    response={"total": total, "jobs": jobs_list}
    return response
def get_application(db: Session, job_id: int, job_seeker_id: int):
    result=(
        db.query(Applications)
        .filter(
            Applications.job_id == job_id,
            Applications.job_seeker_id == job_seeker_id,
        )
        .first()
    )
    return result
def create_application(db: Session, job_id: int, job_seeker_id: int):
    application = Applications(
        job_id=job_id,
        job_seeker_id=job_seeker_id,
        status="APPLIED",
        applied_at=datetime.now(timezone.utc),
    )
    try:
        db.add(application)
        db.commit()
        db.refresh(application)
    except Exception:
        db.rollback()
        return "application failed"
    return application.id
def get_job_by_id(db: Session, job_id: int):
    job= db.query(Jobs).filter(Jobs.id == job_id).first()
    return job
async def get_job_by_id_async(db: Session, job_id: int):
    job= db.query(Jobs).filter(Jobs.id == job_id).first()
    return job
async def get_recruiter_if_approved(db: Session, user_id: int):
    return (
        db.query(Recruiters)
        .filter(Recruiters.user_id == user_id, Recruiters.is_approved == True)
        .first()
    )
def create_job(db:Session,recruiter_user_id:int,title:str,  skills:str,description:str,experience:str,location:str,salary_range:str,job_type:str):
    
    skills_string=",".join(skills) if isinstance(skills,list) else skills
    job = Jobs(
        recruiter_id=recruiter_user_id,
        heading=title.lower(),
        skills=skills_string,
        description=description,
        location=location,
        salary_range=salary_range,
        job_type=job_type,
        experience=experience,
        created_at=datetime.now(),
    )
    skill_names = skills
    db.add(job)
    db.commit()
    db.refresh(job)
    for skill_name in skill_names:

            # Normalize skill
            normalized_skill = skill_name.strip().lower()

            if not normalized_skill:
                continue

            # Check if skill already exists
            existing_skill = (
                db.query(Skills)
                .filter(Skills.skill == normalized_skill)
                .first()
            )

            # Create new skill if not exists
            if not existing_skill:

                new_skill = Skills(
                    skill=normalized_skill
                )

                db.add(new_skill)
                db.flush()
                db.refresh(new_skill)

                existing_skill = new_skill

            # Check if mapping already exists
            existing_mapping = (
                db.query(JobSkills)
                .filter(
                    JobSkills.job_id == job.id,
                    JobSkills.skill_id == existing_skill.id
                )
                .first()
            )

            # Add mapping
            if not existing_mapping:

                job_skill = JobSkills(
                    job_id=job.id,
                    skill_id=existing_skill.id
                )

                db.add(job_skill)
                db.commit()
                db.refresh(job_skill)

            
    return job
def delete_job(db: Session, job_id: int, user_id: int):
    job = db.query(Jobs).filter(Jobs.id == job_id).first()
    job.is_deleted= True
    job.deleted_at= datetime.now(timezone.utc)
    db.commit()
    return {"message": "Job deleted successfully"}

async def get_application_by_id(db: Session, job_id: int):
    appns= (db.query(Applications,JobSeekers).join(JobSeekers,Applications.job_seeker_id==JobSeekers.user_id).filter(Applications.job_id == job_id).all())
    total=len(appns)
    response=[]
    for app,seeker in appns:
        response.append({"application":to_dict(app),"seeker":to_dict(seeker)})
    return {"total":total,"applications":response}
def to_dict(obj):
    result={}
    for k,v in obj.__dict__.items():
        if k.startswith("_"):
            continue
        if isinstance(v,datetime):
            v=v.isoformat()
        result[k]=v
    return result
def get_keywords(db):
    result= db.query(Jobs.heading).all()
    words=set()
    for (heading,)in result:
        if heading:
            cleaned=heading.replace(",","")
            words.add(cleaned.lower())   
    return list(words)
def get_recruiter_id_by_job_id(db: Session, job_id: int):
    recruiter_id = db.query(Jobs.recruiter_id).filter(Jobs.id == job_id).scalar()
    return recruiter_id
def save_job(job_id : int,user_id : int,db: Session,):
    savejob=SavedJobs(job_id=job_id,job_seeker_id=user_id)
    try:
        db.add(savejob)
        db.commit()
        db.refresh(savejob)
    except Exception:
        db.rollback()
        return "Job Save Failed"
    return {"status":"success","message":"Job Saved Successfully"}
def unsave_job(job_id : int,user_id : int,db: Session,):
    stmt=db.query(SavedJobs).filter(SavedJobs.job_id == job_id).filter(SavedJobs.job_seeker_id == user_id).first();
    if not stmt:
        return "Job Unsave Failed"
    try:
        db.delete(stmt)
        db.commit()
    except Exception as e:
        db.rollback()
        return "Job Unsave Failed"
    return {"status":"success","message":"Job Unsaved Successfully"}
def get_saved_jobs(user_id : int,db: Session,):
    saved_jobs=db.query(SavedJobs).filter(SavedJobs.job_seeker_id == user_id).all();
    if saved_jobs:
        return [job.job_id for job in saved_jobs]
    return []
def get_saved_jobs_full(user_id : int,db: Session,):
    saved_jobs_id=db.query(SavedJobs.job_id).filter(SavedJobs.job_seeker_id == user_id).all();
    if saved_jobs_id:
        saved_jobs=db.query(Jobs).filter(Jobs.id.in_([job_id for (job_id,) in saved_jobs_id])).all();
        return [{"job_id": job.id,"heading": job.heading,"description": job.description,"skills": job.skills,
                "location": job.location,"salary_range": job.salary_range,"job_type": job.job_type,"experience": job.experience} 
                for job in saved_jobs]
    return []
def list_job_ids(job_ids: list, job_type: str | None,location: str | None, limit: int, offset: int, db: Session):
    stmt = db.query(Jobs)
    if job_ids:
        stmt=stmt.filter(Jobs.id.in_(job_ids)) 
        stmt=stmt.filter(Jobs.is_deleted == False)
        if location:
            location=location.strip().lower()
            stmt=stmt.filter(Jobs.location == location)
        if job_type:
            job_type=job_type.strip().lower()
            stmt=stmt.filter(Jobs.job_type == job_type) 
        total = stmt.count()
        jobs = stmt.limit(limit).offset(offset).all()
        jobs_list = [job.to_dict() for job in jobs]
        response={"total": total, "jobs": jobs_list}
        return response