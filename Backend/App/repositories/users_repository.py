from sqlalchemy.orm import Session
from models.users import Users, JobSeekers
from models.jobs import Jobs
from models.application import Applications
from models.users import ResumeData,Notification
from models.jobs import Skills
from models.users import UserSkills 
import json
from sqlalchemy import desc
from typing import List
from core.database import sessionLocal
from core.websocket_manager import ConnectionManager
from datetime import datetime, timezone
from core.websocket_manager import manager
from typing import Optional
def get_user_applied_jobs(db: Session,cursor:Optional[str] , user_id: int,limit = 9,):
    count=(db.query(Applications)
        .filter(Applications.job_seeker_id == user_id)
    ).count()
    total_applied=(db.query(Applications)
        .filter(Applications.job_seeker_id == user_id,Applications.status == "APPLIED")
    ).count()
    total_accepted=(db.query(Applications)
        .filter(Applications.job_seeker_id == user_id,Applications.status == "ACCEPTED")
    ).count()
    total_rejected=(db.query(Applications)
        .filter(Applications.job_seeker_id == user_id,Applications.status == "REJECTED")
    ).count()
    if cursor and cursor != "null":
        stmt=(db.query(Jobs,Applications)
        .join(Applications, Applications.job_id == Jobs.id)
        .filter(Applications.job_seeker_id == user_id,Applications.applied_at < cursor).order_by(desc(Applications.applied_at)).limit(limit)
    ).all()
        stmt=to_dict_list(stmt)
        next_cursor=stmt[-1]["applied_at"] if len(stmt) == limit else None
        return {"applications":stmt,"next_cursor":next_cursor,"total":count,"total_applied":total_applied,"total_accepted":total_accepted,"total_rejected":total_rejected}
    stmt = (
        db.query(Jobs,Applications)
        .join(Applications, Applications.job_id == Jobs.id)
        .filter(Applications.job_seeker_id == user_id).order_by(desc(Applications.applied_at)).limit(limit)
    ).all()
    stmt=to_dict_list(stmt)
    next_cursor=stmt[-1]["applied_at"] if len(stmt) == limit else None
    return {"applications":stmt,"next_cursor":next_cursor,"total":count,"total_applied":total_applied,"total_accepted":total_accepted,"total_rejected":total_rejected}
def to_dict_list(query_result):
    result = []
    for job, application in query_result:
        job_dict = job.to_dict()
        job_dict["application_status"] = application.status
        job_dict["applied_at"] = application.applied_at.isoformat()
        result.append(job_dict)
    return result
def get_user(db: Session, user_id: int):
    user = db.query(Users).filter(Users.id == user_id).first()
    return user if user else None
def get_jobseeker_details(db: Session, user_id: int):
    user = db.query(JobSeekers).filter(JobSeekers.user_id == user_id).first()
    if not user:
        return None
    return user
def resume_data(user_id: int,resume_data : dict):
    full_name=json.dumps(resume_data["full_name"]) if "full_name" in resume_data else None
    role=json.dumps(resume_data["job_role"]) if "job_role" in resume_data else None
    email=json.dumps(resume_data["email"]) if "email" in resume_data else None
    phone=json.dumps(resume_data["phone"]) if "phone" in resume_data else None
    skills=json.dumps(resume_data["skills"]) if "skills" in resume_data else None
    experience=json.dumps(resume_data["years_of_experience"]) if "years_of_experience" in resume_data else None
    education=json.dumps(resume_data["education"]) if "education" in resume_data else None
    projects=json.dumps(resume_data["projects"]) if "projects" in resume_data else None
    certifications=json.dumps(resume_data["certifications"]) if "certifications" in resume_data else None
    linkedin=json.dumps(resume_data["linkedin"]) if "linkedin" in resume_data else None
    github=json.dumps(resume_data["github"]) if "github" in resume_data else None    
    summary=json.dumps(resume_data["summary"]) if "summary" in resume_data else None
    db=sessionLocal()
    try:
        existing_resume=db.query(ResumeData).filter(ResumeData.user_id == user_id).first()
        if existing_resume:
            existing_resume.full_name=full_name
            existing_resume.role=role
            existing_resume.email=email
            existing_resume.phone=phone
            existing_resume.skills=skills
            existing_resume.experience=experience
            existing_resume.education=education
            existing_resume.projects=projects
            existing_resume.certifications=certifications
            existing_resume.linkedin=linkedin
            existing_resume.github=github
            existing_resume.summary=summary
            db.commit()
            db.refresh(existing_resume)
            return {"status":"success","message":"Resume Updated Successfully"} 
        resume=ResumeData(user_id=user_id,full_name=full_name,role=role,email=email,phone=phone,skills=skills,experience=experience,
                      education=education,projects=projects,certifications=certifications,linkedin=linkedin,
                      github=github,summary=summary)
        db.add(resume)
        db.commit()
        db.refresh(resume)
    except Exception as e:
        db.rollback()
    finally:
        db.close()
    return {"status":"success","message":"Resume Saved Successfully"}
def update_profile(
    user_id,
    username,
    password,
    skills,
    experience,
    resume_url,
    resume_status,
    db
):
    user = db.query(Users).filter(Users.id == user_id).first()
    jobseeker=db.query(JobSeekers).filter(JobSeekers.user_id == user_id).first()

    if not user:
        return {
            "status": "error",
            "message": "User not found"
        }

    try:

        if password:
            # Replace with password hashing if available
            user.password = password
        if username:
            jobseeker.name = username

        if experience is not None:
            jobseeker.experience = experience

        if resume_url:
            jobseeker.resume_url = resume_url

        if resume_status is not None:
            jobseeker.resume_status = resume_status

        # Process skills
        if skills is not None:

            skill_names = json.loads(skills) if skills else []
            skill_usr=",".join(skill_names) if skill_names else ""

            # Remove old skill mappings
            db.query(UserSkills).filter(
                UserSkills.user_id == user_id
            ).delete()

            for skill_name in skill_names:

                normalized_skill = skill_name.strip().lower()

                if not normalized_skill:
                    continue

                # Find existing skill
                existing_skill = (
                    db.query(Skills)
                    .filter(Skills.skill == normalized_skill)
                    .first()
                )

                # Create skill if not found
                if not existing_skill:

                    existing_skill = Skills(
                        skill=normalized_skill
                    )

                    db.add(existing_skill)
                    db.flush()

                # Create mapping
                user_skill = UserSkills(
                    user_id=user_id,
                    skill_id=existing_skill.id
                )

                db.add(user_skill)

            # Optional: keep JSON/string copy if you have a column
            jobseeker.skills = skill_usr

        db.commit()

        return {
            "status": "success",
            "message": "Profile Updated Successfully"
        }

    except Exception as e:
        db.rollback()

        return {
            "status": "error",
            "message": str(e)
        }
def get_resume_data(user_id):
    db=sessionLocal()
    try:
        response=db.query(ResumeData).filter(ResumeData.user_id == user_id).first()    
        return response
    except Exception:
        db.rollback()
    finally:
        db.close()
    return
async def send_notification(top_candidates: List[int], job_id: int):
    db = sessionLocal()
    try:
        top_candidates = list(set(top_candidates))

        job = db.query(Jobs).filter(Jobs.id == job_id).first()

        if not job:
            return {"status": "error", "message": "Job not found"}

        for user_id in top_candidates:
            user = db.query(Users).filter(Users.id == user_id).first()

            if not user:
                continue

            notification = Notification(
                user_id=user_id,
                job_id=job_id,
                title=job.heading,
                message=f"{job.heading} matches your profile",
                type=job.job_type,
                is_read=False,
                created_at=datetime.now(timezone.utc)
            )

            db.add(notification)
            db.commit()
            db.refresh(notification)

            await manager.send_personal_message(
                user_id,
                {
                    "type": "new_application",
                    "job_id": job_id,
                    "applicant_id": user_id
                }
            )

        return {"status": "success", "message": "Notification Sent Successfully"}

    finally:
        db.close()
async def notification_mark_as_read(notification_id:int,user_id:int,db:Session):
    notification=db.query(Notification).filter(Notification.id == notification_id).filter(Notification.user_id == user_id).first()
    if not notification:
        return {"status":"error","message":"Notification not found"}
    notification.is_read=True
    await manager.send_personal_message(user_id,{"type":"notification_read","notification_id": notification_id,"user_id": user_id})
    db.commit()
    db.refresh(notification)
    return {"status":"success","message":"Notification Marked as Read Successfully"}
def get_notification(user_id:int,db:Session):
    return db.query(Notification).filter((Notification.user_id == user_id),Notification.is_read == False).all()
async def notification_count(user_id:int,db:Session):
    response= db.query(Notification).filter(Notification.user_id == user_id).filter(Notification.is_read == False).count()
    return {"count":response if response else 0}
def get_user_applied_job_ids(user_id:int,db:Session):
    return [application.id for application in db.query(Applications).filter(Applications.job_seeker_id == user_id).all()]