import json

from fastapi import Depends, HTTPException, APIRouter, Request,Query,Form
from sqlalchemy.orm import Session
from core.redis import redis_client as redis
from core.database import get_db
from models.users import Users
from routers.authentication import get_current_user,get_current_user_optional
from core.limiter import limiter
from schemas.jobs import JobRequest
from services import jobs_service
from typing import Optional
import hashlib
from fastapi import BackgroundTasks
from services.vector_service import VectorService
from core.websocket_manager import manager
from schemas.jobs import SaveJobRequest
router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/jobs/{job_id}/applied")
def is_applied(job_id: int,current_user: Users = Depends(get_current_user),db: Session = Depends(get_db),):
    return jobs_service.is_applied(job_id, current_user.id, db)
@router.post("/jobs/{job_id}/apply")
@limiter.limit("5/hour")
async def apply_job(request: Request,job_id: int,db: Session = Depends(get_db),current_user: Users = Depends(get_current_user),):
    result=jobs_service.apply_to_job(job_id, current_user.id, db)
    recruiter_id=jobs_service.get_recruiter_id_by_job_id(db, job_id)
    if recruiter_id:
        await manager.send_personal_message(recruiter_id,{"type":"new_application","job_id": job_id,"applicant_id": current_user.id})
    return result
@router.get("/Jobs/{id}")
async def job_details(id: int, db: Session = Depends(get_db)):
    cache_key=f"job_details:{id}"
    cached_data=await redis.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    result = jobs_service.get_job_details(id, db)
    result=job_to_dict(result)
    await redis.setex(cache_key, 300, json.dumps(result))
    return result
@router.post("/CreateJob")
@limiter.limit("15/hour")
async def create_job(background_tasks: BackgroundTasks,request: Request,data: JobRequest,currentuser: Users = Depends(get_current_user),db: Session = Depends(get_db)):
    return await jobs_service.create_job(background_tasks, data.skills, data.title, data.description,data.experience, data.location, data.salary_range, data.job_type, currentuser.id, db)
@router.delete("/DeleteJob/{job_id}")
@limiter.limit("2/hour")
async def delete_job(request: Request,background_tasks: BackgroundTasks,job_id: int,currentuser: Users = Depends(get_current_user),db: Session = Depends(get_db),):
    return jobs_service.delete_job(background_tasks,job_id, currentuser.id, db)
@router.get("/Applications/{id}")
async def application_details(id: int, db: Session = Depends(get_db)):
    result = await jobs_service.get_application_details(id, db)
    return result
@router.get("/debug/vector")
def debug_vector():
    vector_service=VectorService()
    points, _ = vector_service.client.scroll(collection_name="jobsvectors",limit=10,with_vectors=True)
    return points
def job_to_dict(job):
    return {"id": job.id, "recruiter id": job.recruiter_id,"heading": job.heading,"skills": job.skills, "location": job.location, "salary_range": job.salary_range, "job_type": job.job_type, "description": job.description, "experience": job.experience, "created_at": job.created_at.isoformat(), "is_deleted": job.is_deleted}
@router.get("/keywords")
def get_keywords(db: Session = Depends(get_db)):
    return jobs_service.get_keywords(db)
@router.post("/save")
def save_job(data:SaveJobRequest,db:Session=Depends(get_db),current_user:Users=Depends(get_current_user)):
    return jobs_service.save_job(data.job_id,current_user.id,db)
@router.post("/unsave")
def unsave_job(data:SaveJobRequest,db:Session=Depends(get_db),current_user:Users=Depends(get_current_user)):
    return jobs_service.unsave_job(data.job_id,current_user.id,db)
@router.get("/savedjobs")
def get_saved_jobs(db:Session=Depends(get_db),current_user:Users=Depends(get_current_user)):
    return jobs_service.get_saved_jobs(current_user.id,db)
@router.get("/savedjobsfull")
def get_saved_jobs_full(db:Session=Depends(get_db),current_user:Users=Depends(get_current_user)):
    return jobs_service.get_saved_jobs_full(current_user.id,db)

    
