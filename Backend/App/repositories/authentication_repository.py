from datetime import datetime, timedelta, timezone
from itertools import count
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.users import Users, JobSeekers
from models.recruiters import Recruiters
from models.refreshtoken import RefreshToken
from models.jobs import  Skills
from models.users import UserSkills
import json
from core.database import sessionLocal

def get_user_by_email(db: Session, email: str) -> Users | None:
    return db.query(Users).filter(Users.email == email).first()
def get_user_by_id(db: Session, user_id: int) -> Users | None:
    return db.query(Users).filter(Users.id == user_id).first()
def create_user(db: Session,email: str,password_hash: str,is_verified: bool,verification_token: str,token_expiry: datetime,role: str,is_active: bool=True,) -> Users:
    user = Users(
        email=email,
        password_hash=password_hash,
        role=role,
        is_active=is_active,
        created_at=datetime.now(),
        is_verified=is_verified,
        verification_token=verification_token,  
        token_expiry=token_expiry,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user.id

def create_jobseeker_profile(
    db: Session,
    user_id:int,
    name: str,
    skills: str,
    experience: str,
    resume_url: str,
    resume_status: str,
):
        
        skill_names = json.loads(skills) if skills else []
        skills_string=",".join(skill_names) if skill_names else ""

        # Create Jobseeker Profile
        profile = JobSeekers(
            user_id=user_id,
            name=name,
            skills=skills_string,
            experience=experience,
            resume_url=resume_url,
            resume_status=resume_status,
        )

        db.add(profile)

        # Process Skills
        for skill_name in skill_names:

            # Normalize skill
            normalized_skill = skill_name.strip().lower()

            if not normalized_skill:
                continue

            # Check if skill already exists
            existing_skill = (
                db.query(Skills)
                .filter(Skills.skill == normalized_skill)
                .first()
            )

            # Create new skill if not exists
            if not existing_skill:

                new_skill = Skills(
                    skill=normalized_skill
                )

                db.add(new_skill)
                db.flush()
                db.refresh(new_skill)

                existing_skill = new_skill

            # Check if mapping already exists
            existing_mapping = (
                db.query(UserSkills)
                .filter(
                    UserSkills.user_id == user_id,
                    UserSkills.skill_id == existing_skill.id
                )
                .first()
            )

            # Add mapping
            if not existing_mapping:

                user_skill = UserSkills(
                    user_id=user_id,
                    skill_id=existing_skill.id
                )

                db.add(user_skill)
                db.commit()
                db.refresh(user_skill)

        db.commit()

        db.refresh(profile)

        return profile
def create_recruiter_profile(
    db: Session,
    user_id: int,
    company_name: str,
    company_description: str,
):
    recruiter = Recruiters(
        user_id=user_id,
        company_name=company_name,
        company_description=company_description,
        is_approved=False,
        created_at=datetime.now(),
    )
    db.add(recruiter)
    db.commit()
    db.refresh(recruiter)
    return recruiter
def save_refresh_token(
    db: Session,
    user_id: int,
    token_hash: str,
    expires_days: int = 7,
):
    token = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=datetime.now() + timedelta(days=expires_days),
    )
    db.add(token)
    db.commit()
    db.refresh(token)
    return token
def get_refresh_token_by_hash(db: Session, token_hash: str):
    return (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token_hash == token_hash,
            RefreshToken.is_revoked == False,
        )
        .first()
    )
def revoke_refresh_token(db: Session, token: RefreshToken,user_id: int) -> None:
    db.query(RefreshToken).filter(RefreshToken.user_id == user_id).update({RefreshToken.is_revoked: True})
    db.commit()
def get_any_active_refresh_token(db: Session) -> RefreshToken | None:
    return db.query(RefreshToken).filter(RefreshToken.is_revoked == False).first()
def update_refresh_token(db: Session, token_hash: str, new_token_hash: str):
    stmt=db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).update({RefreshToken.token_hash: new_token_hash})
    db.commit() 
def get_user_id_by_refresh_token(db: Session, refresh_token_hash: str) -> int | None:
    user_id = db.query(RefreshToken.user_id).filter(RefreshToken.token_hash==refresh_token_hash).scalar()
    if user_id:
        return user_id
    return None
def verify_email(db: Session, token: str) -> Users | None:
    user = db.query(Users).filter(Users.verification_token == token).first()
    if user and user.token_expiry > datetime.now():
        user.is_verified = True
        user.verification_token = None
        user.token_expiry = None
        db.commit()
        db.refresh(user)
        return user
    return None
def get_jobseeker_by_id(db: Session, user_id: int):
    skills_ids=db.query(UserSkills.skill_id).filter(UserSkills.user_id == user_id).all()
    skills = [db.query(Skills.skill).filter(Skills.id == skill_id[0]).scalar() for skill_id in skills_ids]
    experience=db.query(JobSeekers.experience).filter(JobSeekers.user_id == user_id).scalar()
    return {"skills":skills,"experience":experience}
def get_skills(db):
    return {"total":(db.query((Skills)).count()),"skills":db.query(Skills).all()}
def reset_password( email: str, new_password: str, db: Session) -> Users | None:
    user = db.query(Users).filter(Users.email == email).first()
    
    if user:
        user.password_hash = new_password
        db.commit()
        db.refresh(user)
        return user
def update_resume_url(user_id :int,resume_url: str,resume_status):
    db=sessionLocal()
    try:
        user = db.query(JobSeekers).filter(JobSeekers.user_id == user_id).first()
        if user:
            user.resume_url = resume_url
            user.resume_status = resume_status
            db.commit()
            db.refresh(user)
    except Exception as e:
        db.rollback()
    finally:
        db.close()


    return{"status":"success","message":"Resume Updated Successfully"}