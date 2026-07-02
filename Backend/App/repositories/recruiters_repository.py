from sqlalchemy.orm import Session
from models.recruiters import Recruiters
from models.application import Applications
from models.jobs import Jobs
from sqlalchemy import func

def get_pending_recruiters(db: Session):
    return db.query(Recruiters).filter(Recruiters.is_approved.is_(False)).all()
def get_recruiter_jobs(db: Session, recruiter_user_id: int):
    return db.query(
        Jobs,
        func.count(Applications.id).label("applications_count")
    ).outerjoin(
        Applications,
        Jobs.id == Applications.job_id
    ).filter(
        Jobs.recruiter_id == recruiter_user_id,Jobs.is_deleted.is_(False)
    ).group_by(Jobs.id).order_by(
        func.count(Applications.id).desc()
    ).all()
    
def get_recruiter_approval_status(db: Session, recruiter_user_id: int) -> bool | None:
    return (
        db.query(Recruiters.is_approved)
        .filter(Recruiters.user_id == recruiter_user_id)
        .scalar()
    )
def get_application_by_user_id_job_id(db: Session, job_id: int, user_id: int):
    return (
        db.query(Applications)
        .filter(Applications.job_id == job_id, Applications.job_seeker_id == user_id)
        .first()
    )
def set_jobseeker_approved(db: Session, job_id: int, user_id: int):
    application = get_application_by_user_id_job_id(db, job_id, user_id)
    application.status = "ACCEPTED"
    db.commit()
    db.refresh(application)
    return application
def set_jobseeker_rejected(db: Session, job_id: int, user_id: int):
    application = get_application_by_user_id_job_id(db, job_id, user_id)
    application.status = "REJECTED"
    db.commit()
    db.refresh(application)
    return application
def get_applications_by_id(db: Session, user_id: int):
    job_ids = db.query(Jobs.id).filter(Jobs.recruiter_id == user_id).all()
    job_ids = [job_id for (job_id,) in job_ids]  # Unpack the tuples
    result = db.query(func.count(Applications.id), Applications.job_id).filter(Applications.job_id.in_(job_ids)).group_by(Applications.job_id).all()
    return {job_id: count for count, job_id in result}
def get_total_jobs(db: Session, user_id: int):
    return db.query(func.count(Jobs.id)).filter(Jobs.recruiter_id == user_id).scalar()
def get_total_applications_by_job_id(db: Session, job_id: int):
    response=db.query(Applications).filter(Applications.job_id == job_id).all()
    for app in response:
        result=[{"job_id":app.job_id,"job_seeker_id":app.job_seeker_id,"status":app.status,"applied_at":app.applied_at} for app in response]
    return result