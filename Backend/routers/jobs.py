
from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from datetime import datetime,timezone
from models import Users,Recruiters
from schemas import JobRequest
from models import Users,Recruiters,Jobs,Applications
from routers.authentication import get_current_user
router=APIRouter(prefix="/jobs",tags=["jobs"])
@router.get("/jobs")
def joblist(db:Session=Depends(get_db)):
    res=(db.query(Jobs).all())
    return res
@router.post("/Jobs/search")
def searchjob(search:str,db:Session=Depends(get_db)):
    res=(db.query(Jobs).filter(or_(Jobs.heading.like(f"%{search}%"),
                             Jobs.skills.like(f"%{search}%"),
                             Jobs.description.like(f"%{search}%"))).all())
    return res
@router.get("/fJobs")
def get_jobs(search: str,job_type: str , location: str ,db: Session = Depends(get_db)):
    stmt=db.query(Jobs)
    if search:
        stmt =stmt.filter(
            or_(
                Jobs.heading.like(f"%{search}%"),
                Jobs.skills.like(f"%{search}%"),
                Jobs.description.like(f"%{search}%")
            )
        )

    if job_type:
        stmt = stmt.filter(Jobs.job_type == job_type)
    if location:
        stmt = stmt.filter(Jobs.location == location)

    return stmt.all()
@router.get("/jobs/{job_id}/applied")
def is_applied(
    job_id: int,
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)):
    applied = db.query(Applications).filter(
        Applications.job_id == job_id,
        Applications.job_seeker_id == current_user.id
    ).first()

    return {"applied": applied is not None}
@router.post("/jobs/{job_id}/apply")
def apply_job(job_id: int,db: Session = Depends(get_db),current_user: Users = Depends(get_current_user)):
    job = db.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    existing = db.query(Applications).filter(
        Applications.job_id == job_id,
        Applications.job_seeker_id == current_user.id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Already applied"
        )
    application = Applications(
        job_id=job_id,
        job_seeker_id=current_user.id,
        status="APPLIED",
        applied_at=datetime.now(timezone.utc)
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return {
        "message": "Appllied successfully",
        "application_id": application.id
    }
@router.get("/Jobs/{id}")
def job_details(id:int,db:Session=Depends(get_db)):
    stmt=db.query(Jobs).filter(Jobs.id==id)
    job=stmt.first()
    return job
@router.post("/CreateJob")
def create_job(data:JobRequest,currentuser:Users=Depends(get_current_user),db:Session=Depends(get_db)):
    stmt = db.query(Recruiters).filter(Recruiters.user_id == currentuser.id,Recruiters.is_approved==True)
    res=stmt.first()
    if not res:
        raise HTTPException(status_code=403, detail="Recruiter not Approved")
    model = Jobs(
            recruiter_id=currentuser.id,
            heading=data.title,
            skills=data.skills,
            description=data.description,
            location=data.location,
            salary_range=data.salary_range,
            job_type=data.job_type,
            created_at=datetime.now())
    db.add(model)
    db.commit()
    return {"message": "Job Creation Successful"}