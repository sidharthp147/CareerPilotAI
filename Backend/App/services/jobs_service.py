import hashlib
import json
from tools.Search_tool import search_tool
from tools.Ranking_tool import rank_jobs
from core.redis import redis_client as redis
from sqlalchemy.orm import Session
from fastapi import HTTPException
from repositories import authentication_repository, jobs_repository, users_repository
from services.vector_service import VectorService
from sentence_transformers import SentenceTransformer
from services.Notification_service import notifications
model=SentenceTransformer('all-MiniLM-L6-v2')
from core.database import sessionLocal
import logging
logger=logging.getLogger(__name__)

async def list_jobs(db: Session,current_user: int | None, search: str | None, job_type: str | None, location: str | None, limit: int, offset: int,):
    from llm.Ranking_jobs_llm import ranking_llm
    ids=[]
    user=users_repository.get_user(db,current_user) if current_user else None
    if current_user is None or user.role=="RECRUITER" or user.role=="ADMIN" or user.role is None:
            response= await jobs_repository.list_jobs(ids, search, job_type,None,None,None, location, limit, offset,db)
            if response["total"]==0:
                return {"total": 0, "jobs": []}
            return response
    if search:
        
        search_response=await search_tool(search,job_type,location,limit,offset,db)
        jobs=search_response["jobs"] if "jobs" in search_response else []
        total=search_response["total"]
        apply=search_response["apply"] if "apply" in search_response else False
        count=search_response["count"] if "count" in search_response else 0
        location=search_response["location"] if "location" in search_response else None
        job_type=search_response["job_type"] if "job_type" in search_response else None
        cache_key=f"cache:jobs:{hashlib.md5(search.encode()).hexdigest()}:{job_type}:{location}"
        cached_data=await redis.get(cache_key)
        ##if cached_data:
            ##return json.loads(cached_data)
        vector_service=VectorService()
        resume_data=vector_service.get_resume_data(user.id)
        userdetails={}
        if resume_data is None:
            userdetails=get_user_details(db,current_user)
            userdetails["user_title"]=search
            userdetails["user_location"]=location
            userdetails["user_job_type"]=job_type
        else:
            userdetails["user_title"]=resume_data["job_role"]
            userdetails["user_location"]=location
            userdetails["user_job_type"]=job_type
            userdetails["user_skills"]=resume_data["skills"]
        if jobs==[]:
            return {"total": 0, "jobs": []}
        ranked_jobs=await rank_jobs(jobs,userdetails)
        if ranked_jobs:
            jobs=ranked_jobs["jobs"]
            total=ranked_jobs["total"]
            jobs= await ranking_llm(jobs,userdetails)
            jobs=jobs["jobs"]
            jobs=sorted(jobs,key=lambda x:x.get("final_score",0),reverse=True)
        if job_type:
            jobs=[job for job in jobs if job["job_type"].lower()==job_type.lower()]
            total=len(jobs)
        if location:
            jobs=[job for job in jobs if job["location"].lower()==location.lower()]
            total=len(jobs)
        if apply and count>0:
           
            await redis.setex(cache_key, 300, json.dumps({"total": total, "jobs": jobs, "apply":apply,"count":count,"action": "confirmation_required"}))
            return {"total": total, "jobs": jobs, "apply":apply,"count":count,"action": "confirmation_required"}
        await redis.setex(cache_key, 300, json.dumps({"total": total, "jobs": jobs}))
        return {"total": total, "jobs": jobs}
    cache_key=f"cache:jobs:{hashlib.md5(job_type.encode()).hexdigest()}:{hashlib.md5(location.encode()).hexdigest()}"
    cached_data=await redis.get(cache_key)
    ##if cached_data:
      ##return json.loads(cached_data)
    response= await jobs_repository.list_jobs(None, search, job_type,None,None,None, location, limit, offset,db)
    await redis.setex(cache_key, 300, json.dumps(response))
    return response
def is_applied(job_id: int, user_id: int, db: Session):
    applied = jobs_repository.get_application(db, job_id, user_id)
    if applied is None:
        return {"continuee": True}
    return {"applied": applied}

def apply_to_job(job_id: int, user_id: int, db: Session):
    job = jobs_repository.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    existing = jobs_repository.get_application(db, job_id, user_id)
    if existing:
        raise HTTPException(status_code=400, detail="Already applied")

    application = jobs_repository.create_application(db, job_id, user_id)
    return {
        "message": "Applied successfully",
        "application_id": application,
    }

def get_job_details(job_id: int, db: Session):
    job = jobs_repository.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

async def create_job(background_tasks,skills : list,title : str,description : str,experience : str,location : str,salary_range : str,job_type : str, user_id, db):
    recruiter = await jobs_repository.get_recruiter_if_approved(db, user_id)
    if not recruiter:
        raise HTTPException(status_code=403, detail="Recruiter not Approved")

    job=jobs_repository.create_job(
        db,
        recruiter_user_id=user_id,
        title=title,
        skills=skills,
        description=description,
        location=location,
        salary_range=salary_range,
        job_type=job_type,
        experience=experience,
    )
    try:
        job = await jobs_repository.get_job_by_id_async(db, job.id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        text = f"{job.heading} {job.description} {job.skills} {job.location} {job.salary_range} {job.job_type}"
        embedding = get_embedding(text)

    except Exception as e:
        logger.error(e)

   
    await job_embedding(embedding,job)
    await notifications(embedding,job.id)
    return {"message": "Job Creation Successful"}
def delete_job(background_tasks,job_id: int, userid:int, db: Session,):
    job = jobs_repository.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.recruiter_id != userid:
        raise HTTPException(status_code=403, detail="Not authorized to delete this job")
    background_tasks.add_task(embedding_removal, job_id)
    return  jobs_repository.delete_job(db, job_id, userid)
async def get_application_details(job_id: int, db: Session):
    appns = await jobs_repository.get_application_by_id(db, job_id)
    if not appns:
        raise HTTPException(status_code=404, detail="Job not found")
    return appns
async def job_embedding(embedding: list[float], job):
    vector_service = VectorService()
    vector_service.store_job_embedding(job, embedding)
def embedding_removal(job_id: int):
    db= sessionLocal()
    try:
        job=jobs_repository.get_job_by_id(db, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        vector_service = VectorService()
        vector_service.remove_job_embedding(job_id)
    except Exception as e:
        logger.error(e)
    finally:
        db.close()
def get_keywords(db: Session):
    return jobs_repository.get_keywords(db)
def get_user_details(db:Session,user_id:int):
    user=authentication_repository.get_jobseeker_by_id(db,user_id)
    if user:
        user_skills=user["skills"]
        user_experience=user["experience"]
        return {"user_skills":user_skills,"user_experience":user_experience}
    else:
        return {"error": "User not found"}
def get_recruiter_id_by_job_id(db: Session, job_id: int):
    return jobs_repository.get_recruiter_id_by_job_id(db, job_id)
def save_job(job_id,user_id,db):
    return jobs_repository.save_job(job_id,user_id,db)
def unsave_job(job_id,user_id,db):
    return jobs_repository.unsave_job(job_id,user_id,db)
def get_saved_jobs(user_id,db):
    return jobs_repository.get_saved_jobs(user_id,db)
def get_embedding(text: str) -> list[float]:
    return model.encode(text).tolist()

def get_saved_jobs_full(user_id,db):
    return jobs_repository.get_saved_jobs_full(user_id,db)