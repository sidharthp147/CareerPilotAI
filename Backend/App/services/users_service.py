from sqlalchemy.orm import Session
from models.users import Users
from repositories import users_repository
from services.vector_service import VectorService
from repositories import jobs_repository
from services.model_service import model
from sentence_transformers.util import cos_sim
from core.redis import redis_client as redis
import json
def get_user_applications(cursor: str | None,user_id: int, db: Session):
    return users_repository.get_user_applied_jobs(db,cursor, user_id)
def get_jobseeker_profile(user_id: int, db: Session):
    user = users_repository.get_jobseeker_details(db, user_id)
    if user:
        return user
    else:
        return {"error": "User not found"}
def update_profile(user_id,username,password,skills,experience,resume_url,resume_status,db):
    return users_repository.update_profile(user_id,username,password,skills,experience,resume_url,resume_status,db)
async def get_recommended_jobs(user_id,db):
    cache_key=f"cache:recommended_jobs:{user_id}"
    cached_data=await redis.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    try:
        vector_service=VectorService()
        resume_embedding=vector_service.get_recommendation_vectors(user_id)
        if resume_embedding:
            recommended_jobs=vector_service.search_vectors(resume_embedding.vector,50)
            data=vector_service.get_resume_data(user_id)
            user_role=data["job_role"] if data["job_role"] else ""
            user_experience=int(data["experience"]) if data["experience"] else 0
            user_skills=data["skills"] if data["skills"] else ""
            if user_skills:
                user_skills=",".join(user_skills)
            score_map={points.id:points.score for points in recommended_jobs.points if points.score>0.30}
            ids=[points.id for points in recommended_jobs.points if points.score>0.30]
            already_applied_jobs=users_repository.get_user_applied_job_ids(user_id,db)
            ids=[job_id for job_id in ids if job_id not in already_applied_jobs]

            if ids:
                response= await jobs_repository.list_jobs(ids, None, None,None,None,None, None, 50, 0,db)
                jobs=response["jobs"]
                total=response["total"]
                for job in jobs:
                    job_experience=int(job["experience"]) if job["experience"] else 0
                    job_skills=job["skills"] if job["skills"] else ""
                    job_role=job["heading"] if job["heading"] else ""
                    if user_experience==0 and job_experience==0:
                        experience_score=1
                        
                    elif user_experience==0:
                        experience_score=0
                        
                    elif job_experience==user_experience:
                        experience_score=1
                        
                    elif job_experience>user_experience:
                            experience_score=(user_experience/job_experience)
                            
                    else:
                        experience_score=1
                    skills_score=float(cos_sim(model.encode(user_skills,convert_to_tensor=True),model.encode(job_skills,convert_to_tensor=True)))
                    role_score=float(cos_sim(model.encode(user_role,convert_to_tensor=True),model.encode(job_role,convert_to_tensor=True)))
                    job["final_score"]=((score_map[job["id"]])*0.3+(experience_score)*0.2+(role_score)*0.2+(skills_score)*0.3)
                jobs_sorted=sorted(jobs,key=lambda x:x.get("final_score",0),reverse=True)
                await redis.setex(cache_key, 300, json.dumps({"jobs":jobs_sorted,"total":total}))
                return {"jobs":jobs_sorted,"total":total,"message":"Recommended Jobs Based On Your Resume"}
        if resume_embedding is None:
            return {"jobs":[],"total":0,"message":"Please Upload Resume For Recommendations"}
        return {"jobs":[],"total":0,"message":"No Jobs Found For Recommendations"}
    except Exception as e:
        return {"jobs":[],"total":0,"message":"Error Occurred While Fetching Recommended Jobs"} 
async def notification_mark_as_read(notification_id,user_id,db):
    return await users_repository.notification_mark_as_read(notification_id,user_id,db)
def get_notification(user_id,db):
    return users_repository.get_notification(user_id,db)
async def notification_count(user_id,db):
    return await users_repository.notification_count(user_id,db)