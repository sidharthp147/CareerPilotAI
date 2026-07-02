from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from core.database import get_db
from models.users import Users
from routers.authentication import get_current_user, require_role
from services import users_service
from fastapi import Request,Form
from fastapi import UploadFile,File,HTTPException,BackgroundTasks
from routers.authentication import resume_upload
from llm import Resume_extraction_llm
from services import authentication_service
import json
from core.redis import redis_client as redis
from core.limiter import limiter
router = APIRouter(prefix="/users", tags=["users"])
@router.get("/UserApplication")
def userapplication(cursor: str | None,currentuser: Users = Depends(get_current_user),db: Session = Depends(get_db),):
    return users_service.get_user_applications(cursor,currentuser.id, db)
@router.get("/UserRecommendedJobs")
async def userdashboard(db: Session = Depends(get_db),currentuser: Users = Depends(get_current_user),):
    cache_key = f"user_recommended_jobs_{currentuser.id}"
    cached_data = await redis.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    response= await users_service.get_recommended_jobs(currentuser.id, db)
    await redis.setex(cache_key, 300, json.dumps(response))
    return response
@router.get("/Userprofiles")
def userprofile(currentuser: Users = Depends(get_current_user),db: Session = Depends(get_db),):
    return users_service.get_jobseeker_profile(currentuser.id, db)

@router.put("/updateprofile")
@limiter.limit("1/hour")
async def update_profile(request: Request,background_tasks: BackgroundTasks,username: Optional[str]=Form(None),password: Optional[str]=Form(None),confirmpassword: Optional[str]=Form(None),selectedSkills: Optional[str]=Form(None),experience: Optional[str]=Form(None),file: Optional[UploadFile] =File(None),db: Session = Depends(get_db),current_user: Users = Depends(get_current_user)):
    if file is None:
        resume_url=None
    if password:
        if password != confirmpassword:
            raise HTTPException(status_code=400, detail="Passwords do not match")
    if password:
        password=authentication_service.hash_password(password)
    if current_user.role != "USER":
        raise HTTPException(status_code=403, detail="Not Authenticated")
    if file:
        resume_url= await resume_upload(background_tasks,user_id=current_user.id,file=file)
        resume_status="uploading"
    if resume_url:
        resume_status="uploaded"
        background_tasks.add_task(Resume_extraction_llm.resume_extraction,file_url=resume_url,user_id=current_user.id)
        return users_service.update_profile(current_user.id,username,password,selectedSkills,experience,resume_url,resume_status, db, ) 
    return users_service.update_profile(current_user.id,username,password,selectedSkills,experience,None,None, db) 
@router.get("/notifications")
def notification(request: Request,db: Session = Depends(get_db),current_user: Users = Depends(get_current_user)):
    return users_service.get_notification(current_user.id,db)   
@router.put("/notifications/{notification_id}")
async def notification_mark_as_read(notification_id: int,db: Session = Depends(get_db),current_user: Users = Depends(get_current_user)):
    return await users_service.notification_mark_as_read(notification_id, current_user.id, db)
@router.get("/aaaaaaaaaaa")
async def notification_count(current_user: Users = Depends(get_current_user),db: Session = Depends(get_db)):
    return await users_service.notification_count(current_user.id,db)
    