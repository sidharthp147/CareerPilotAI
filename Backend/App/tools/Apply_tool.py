from fastapi import HTTPException
from sqlalchemy.orm import Session
from services import jobs_service
async def apply_to_jobs(user_id: int, job_ids: list, db: Session):
    results = []
    for job_id in job_ids:
        try:
            is_applied_result = jobs_service.is_applied(job_id, user_id, db)
            if "applied" in is_applied_result:
                results.append({"job_id": job_id, "status": "already_applied", "application_id": is_applied_result["applied"].id})
                continue
            result = jobs_service.apply_to_job( job_id,user_id, db)
            results.append({"job_id": job_id, "status": "success", "application_id": result["application_id"]})
        except HTTPException as e:
            results.append({"job_id": job_id, "status": "error", "detail": e.detail})
    return results