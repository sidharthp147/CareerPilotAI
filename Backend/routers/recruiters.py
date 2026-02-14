from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Users,Recruiters
from fastapi import APIRouter
from models import Users,Recruiters,Jobs
from routers.authentication import get_current_user
router=APIRouter(prefix="/recruiters",tags=["recruiters"])
@router.get("/recruiters")
def fetch_recruiters(db:Session=Depends(get_db)):
    stmt=db.query(Recruiters).filter(Recruiters.is_approved.is_(False))
    res=stmt.all()
    return res

@router.get("/RecruiterDashboard")
def recruiterdashboard(currentuser:Users=Depends(get_current_user),db:Session=Depends(get_db)):
    if (currentuser.role=="RECRUITER"):
        stmt1=db.query(Jobs).filter(Jobs.recruiter_id==currentuser.id)
        res1=stmt1.all()
        stmt2=db.query(Recruiters.is_approved).filter(Recruiters.user_id==currentuser.id)
        res2=stmt2.scalar()
        return {"res1":res1,"res2":res2}
    else:
        raise HTTPException(status_code=401, detail="Wrong data")