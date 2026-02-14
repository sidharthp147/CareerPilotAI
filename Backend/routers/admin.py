from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException
from sqlalchemy import func
from database import get_db
from models import JobSeekers,Recruiters,Jobs
router=APIRouter(prefix="/admin",tags=["admin"])
@router.get("/AdminDashboard")
def admindashboard(db:Session=Depends(get_db)):
        total_users=db.query(func.count(JobSeekers.user_id)).scalar()
        total_recruiters=db.query(func.count(Recruiters.user_id)).scalar()
        total_jobs=db.query(func.count(Jobs.id)).scalar()
        return {"total_users":total_users,"total_recruiters":total_recruiters,"total_jobs":total_jobs}
@router.get("/recruiters")
def fetch_recruiters(db:Session=Depends(get_db)):
    stmt=db.query(Recruiters).filter(Recruiters.is_approved.is_(False))
    res=stmt.all()
    return res

@router.post("/{id}/approve")
def approve_recruiter(id: int, db: Session = Depends(get_db)):
    recruiter = db.query(Recruiters).filter(Recruiters.user_id == id).first()

    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter not found")

    recruiter.is_approved = True
    db.commit()
    db.refresh(recruiter)

    return {
        "message": "Recruiter approved successfully",
        "recruiter_id": recruiter.user_id
    }
@router.post("/{id}/reject")
def reject_recruiter(id: int, db: Session = Depends(get_db)):
    recruiter = db.query(Recruiters).filter(Recruiters.user_id == id).first()

    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter not found")

    recruiter.is_approved = None
    db.commit()
    db.refresh(recruiter)

    return {
        "message": "Recruiter rejected successfully",
        "recruiter_id": recruiter.user_id
    }
