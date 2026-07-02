from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.users import Users
from routers.authentication import require_role
from services import recruiters_service
from core.websocket_manager import manager
from core.redis import redis_client as redis
import json
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/recruiters", tags=["recruiters"])
@router.get("/recruiters")
def fetch_recruiters(db: Session = Depends(get_db)):
    return recruiters_service.list_pending_recruiters(db)
@router.get("/RecruiterDashboard")
async def recruiterdashboard(currentuser: Users = Depends(require_role(["RECRUITER"])),db: Session = Depends(get_db),):
   result=recruiters_service.get_recruiter_dashboard(currentuser.id, db)
   result["res1"] = [{"id": job.id, "title": job.heading,"skills": job.skills, "description": job.description, "location": job.location, "job_type": job.job_type,"created_at": job.created_at,"applications_count":count } for job,count in result["res1"]]
   result["res2"] = bool(result["res2"])
   response={"res1": result["res1"], "res2": result["res2"], "res3": result["res3"], "res4": result["res4"]}
   return response
@router.post("/user/{job_id}/{user_id}/approve")
async def approve_jobseeker(job_id: int, user_id: int, db: Session = Depends(get_db)):
    await manager.send_personal_message(user_id,{"type":"Approved","job_id": job_id,"applicant_id": user_id})
    return recruiters_service.approve_jobseeker(db, job_id, user_id)
@router.post("/user/{job_id}/{user_id}/reject")
async def reject_jobseeker(job_id: int, user_id: int, db: Session = Depends(get_db)):
    await manager.send_personal_message(user_id,{"type":"Rejected","job_id": job_id,"applicant_id": user_id})
    return recruiters_service.reject_jobseeker(db, job_id, user_id)
@router.post("/rankcandidates/{job_id}")
async def rank_candidate(job_id: int, db: Session = Depends(get_db)):
    cache_key = f"rank_candidates:{job_id}"
    cache_data=await redis.get(cache_key)
    if cache_data:
        return json.loads(cache_data)
    response=  recruiters_service.rank_candidates(db, job_id)
    await redis.setex(cache_key, 300, json.dumps(jsonable_encoder(response)))
    return response