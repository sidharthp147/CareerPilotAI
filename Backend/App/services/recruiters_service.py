from sqlalchemy.orm import Session
from models.users import Users
from repositories import recruiters_repository,jobs_repository
from fastapi import HTTPException
from tools.Candidate_ranking_tool import rank_candidates_tool
from core.redis import redis_client as redis
import json
def list_pending_recruiters(db: Session):
    return recruiters_repository.get_pending_recruiters(db)
def get_recruiter_dashboard(user_id: int, db: Session):
    jobs = recruiters_repository.get_recruiter_jobs(db, user_id)
    applications_count = recruiters_repository.get_applications_by_id(db, user_id)
    is_approved = recruiters_repository.get_recruiter_approval_status(db, user_id)
    total=recruiters_repository.get_total_jobs(db, user_id)
    return {"res1": jobs, "res2": is_approved, "res3": applications_count, "res4": total}
def approve_jobseeker(db: Session, job_id: int, user_id: int) -> dict:
    user = recruiters_repository.get_application_by_user_id_job_id(db,job_id, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Recruiter not found")
    recruiters_repository.set_jobseeker_approved(db, job_id, user_id)
    return {
        "message": "Recruiter approved successfully",
        "recruiter_id": user.id,
    }
def reject_jobseeker(db: Session, job_id: int, user_id: int) -> dict:
    user = recruiters_repository.get_application_by_user_id_job_id(db,job_id, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    recruiters_repository.set_jobseeker_rejected(db, job_id, user_id)
    return {
        "message": "Recruiter rejected successfully",
        "recruiter_id": user.id,
    }
def rank_candidates(db: Session, job_id: int) :
    applicants=recruiters_repository.get_total_applications_by_job_id(db, job_id)
    job=jobs_repository.get_job_by_id(db,job_id)
    ranked_applicants=rank_candidates_tool(db,job,applicants)
    return ranked_applicants
    