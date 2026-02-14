
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Users,Jobs
from fastapi import APIRouter
from models import Users,Applications
from routers.authentication import get_current_user
router=APIRouter(prefix="/users",tags=["users"])
@router.get("/UserDashboard")
def userdashboard(currentuser:Users=Depends(get_current_user),db:Session=Depends(get_db)):
    if (currentuser.role=="USER"):
        stmt=db.query(Jobs).join(Applications,Applications.job_id==Jobs.id).filter(Applications.job_seeker_id==currentuser.id)
        res=stmt.all()
        return res
    else:
        raise HTTPException(status_code=401, detail="Wrong data")