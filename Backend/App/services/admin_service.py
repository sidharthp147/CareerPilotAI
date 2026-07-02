from sqlalchemy.orm import Session
from fastapi import HTTPException
from repositories import admin_repository

def get_analytics(db: Session) -> dict:
    return admin_repository.get_analytics(db)
def list_pending_recruiters(db: Session):
    return admin_repository.get_pending_recruiters(db)
def approve_recruiter(db: Session, user_id: int) -> dict:
    recruiter = admin_repository.get_recruiter_by_user_id(db, user_id)
    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter not found")
    admin_repository.set_recruiter_approved(db, recruiter, True)
    return {
        "message": "Recruiter approved successfully",
        "recruiter_id": recruiter.user_id,
    }
def reject_recruiter(db: Session, user_id: int) -> dict:
    recruiter = admin_repository.get_recruiter_by_user_id(db, user_id)
    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter not found")
    admin_repository.set_recruiter_rejected(db, recruiter, False)
    return {
        "message": "Recruiter rejected successfully",
        "recruiter_id": recruiter.user_id,
    }