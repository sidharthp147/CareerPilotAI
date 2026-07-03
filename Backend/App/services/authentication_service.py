from datetime import datetime, timedelta, timezone
import smtplib
from typing import Any, Dict
from fastapi import HTTPException, BackgroundTasks
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from schemas.recruiters import RecruiterRequest
from schemas.auth import LoginRequest
from repositories import authentication_repository
import hashlib
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_DAYS,SECRET_KEY,SMTP_SERVER,SMTP_PORT,SMTP_EMAIL,SMTP_PASSWORD,ALGORITHM
import uuid
from email.mime.text import MIMEText
import os
import secrets
access_token_expires_min=ACCESS_TOKEN_EXPIRE_MINUTES
refresh_token_expire_days=REFRESH_TOKEN_EXPIRE_DAYS

# =========================
# PASSWORD CONFIG
# =========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET =SECRET_KEY
ALGORITHM = ALGORITHM


# =========================
# TOKEN HELPERS
# =========================

def generate_verification_token():
    return str(uuid.uuid4())


def hash_password(password: str):

    if len(password) > 128:
        raise HTTPException(
            status_code=400,
            detail="Password too long"
        )

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def hash_token(token: str):
    return hashlib.sha256(
        token.encode()
    ).hexdigest()


def verify_token(
    plain_token: str,
    hashed_token: str
):

    return pwd_context.verify(
        plain_token,
        hashed_token
    )


# =========================
# JWT TOKENS
# =========================

def create_token(
    data: Dict[str, Any]
):

    to_encode = data.copy()
    expire = (
        datetime.now(timezone.utc)
        + timedelta(minutes=int(access_token_expires_min))
    )

    to_encode.update({
        "exp": int(expire.timestamp())
    })
    return jwt.encode(
        to_encode,
        SECRET,
        algorithm=ALGORITHM
    )


def create_refresh_token(
    data: Dict[str, Any]
):

    to_encode = data.copy()
    expire = (
        datetime.now(timezone.utc)
        + timedelta(days=int(refresh_token_expire_days))
    )

    to_encode.update({
        "exp": int(expire.timestamp())
    })

    return jwt.encode(
        to_encode,
        SECRET,
        algorithm=ALGORITHM
    )


def decode_token(token: str) -> dict:

    try:

        return jwt.decode(
            token,
            SECRET,
            algorithms=[ALGORITHM]
        )

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


# =========================
# LOGIN
# =========================

def login_user(
    data: LoginRequest,
    db: Session
):

    user = authentication_repository.get_user_by_email(
        db,
        data.email
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    # Verify password
    if user.role!="ADMIN" and not verify_password(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User is not active"
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=401,
            detail="User is not verified"
        )

    token = create_token({
        "sub": str(user.id),
        "role": str(user.role)
    })

    refresh_token = create_refresh_token({
        "sub": str(user.id)
    })

    return {
        "user": user,
        "token": token,
        "refresh_token": refresh_token,
    }


# =========================
# REFRESH TOKEN
# =========================

def save_refresh_for_user(
    db: Session,
    user_id: int,
    refresh_token: str
):

    refresh_token_hash = hash_token(
        refresh_token
    )

    authentication_repository.save_refresh_token(
        db,
        user_id,
        refresh_token_hash
    )


# =========================
# REGISTER JOBSEEKER
# =========================

def register_jobseeker(
    background_tasks: BackgroundTasks,
    email,
    password,
    confirmpassword,
    username,
    skills,
    experience,
    resume_url,
    resume_status,
    db: Session
) -> dict:

    if password != confirmpassword:
        raise HTTPException(
            status_code=400,
            detail="Password Doesn't Match"
        )

    token = generate_verification_token()

    # Create User
    user_id = authentication_repository.create_user(
        db=db,
        email=email,
        password_hash=hash_password(password),
        is_verified=False,
        verification_token=token,
        token_expiry=datetime.now() + timedelta(minutes=60),
        role="USER"
    )
   

    # Create Profile
    authentication_repository.create_jobseeker_profile(
        db=db,
        user_id=user_id,
        name=username,
        skills=skills,
        experience=experience,
        resume_url=resume_url,
        resume_status=resume_status
    )

    if user_id:

        background_tasks.add_task(
            send_verification_email,
            email=email,
            token=token
        )

        return {
            "message":
            "Registration Successful. Check your email for verification."
        }

    raise HTTPException(
        status_code=400,
        detail="Registration Failed"
    )


# =========================
# REGISTER RECRUITER
# =========================

def register_recruiter(
    data,
    db: Session,
    background_tasks: BackgroundTasks
):
    user=authentication_repository.get_user_by_email(db,data.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )
    if not user:
        if data.password != data.confirmpassword:
            raise HTTPException(
                status_code=400,
                detail="Password Doesn't Match"
            )

        token = generate_verification_token()

        user = authentication_repository.create_user(
            db=db,
            email=data.email,
            password_hash=hash_password(data.password),
            role="RECRUITER",
            is_verified=False,
            verification_token=token,
            token_expiry=datetime.now() + timedelta(minutes=60),
        )

        authentication_repository.create_recruiter_profile(
            db=db,
            user_id=user,
            company_name=data.company_name,
            company_description=data.company_description,
        )

        if user:

            background_tasks.add_task(
                send_verification_email,
                email=data.email,
                token=token
            )

            return {
                "message":
                "Registration Successful. Check your email for verification."
            }
        
        raise HTTPException(
            status_code=400,
            detail="Registration Failed"
        )
    raise HTTPException(
            status_code=404,
            detail="Email id exists,Try with another email"
        )


# =========================
# ROTATE REFRESH TOKEN
# =========================

def rotate_refresh_token(
    refresh_token: str | None,
    db: Session
):

    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token missing"
        )

    token_hash = hash_token(refresh_token)

    db_token = (
        authentication_repository
        .get_refresh_token_by_hash(
            db,
            token_hash
        )
    )

    if not db_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    exp_timestamp = db_token.expires_at

    if not exp_timestamp:

        authentication_repository.revoke_refresh_token(
            db,
            db_token,
            db_token.user_id
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    if exp_timestamp.tzinfo is None:
        exp_datetime = exp_timestamp.replace(
            tzinfo=timezone.utc
        )
    else:
        exp_datetime = exp_timestamp.astimezone(
            timezone.utc
        )

    now = datetime.now(timezone.utc)

    if exp_datetime < now:

        authentication_repository.revoke_refresh_token(
            db,
            db_token,
            db_token.user_id
        )

        raise HTTPException(
            status_code=401,
            detail="Refresh token expired"
        )

    refresh_token = create_refresh_token({
        "sub": str(db_token.user_id)
    })

    new_token_hash = hash_token(
        refresh_token
    )

    authentication_repository.update_refresh_token(
        db,
        token_hash,
        new_token_hash
    )

    access_token = create_token({
        "sub": str(db_token.user_id)
    })

    return {
        "token": refresh_token,
        "access_token": access_token
    }


# =========================
# LOGOUT
# =========================

def logout_user(
    refresh_token: str | None,
    db: Session
):

    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token missing"
        )

    token_hash = hash_token(refresh_token)

    db_token = (
        authentication_repository
        .get_refresh_token_by_hash(
            db,
            token_hash
        )
    )

    if db_token:

        authentication_repository.revoke_refresh_token(
            db,
            db_token,
            db_token.user_id
        )

    return {
        "message": "Logged out successfully"
    }


# =========================
# EMAIL
# =========================

def send_verification_email(
    email: str,
    token: str
):

    verify_url = (
        f"https://careerpilotai-production-d61a.up.railway.app/verify-email?token={token}"
    )

    subject = "Verify your email"

    body = (
        f"Click the link to verify your email:\n\n"
        f"{verify_url}"
    )

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] =SMTP_EMAIL
    msg["To"] = email

    with smtplib.SMTP(
        SMTP_SERVER,
        int(SMTP_PORT)
    ) as server:

        server.starttls()

        server.login(
            SMTP_EMAIL,
            SMTP_PASSWORD)

        server.send_message(msg)


# =========================
# RESEND VERIFICATION
# =========================

def resend_verification_email(
    email: str,
    db: Session,
    background_tasks: BackgroundTasks
):

    user = authentication_repository.get_user_by_email(
        db,
        email
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.is_verified:
        return {
            "message": "Email already verified"
        }

    token = generate_verification_token()

    user.verification_token = token

    user.token_expiry = (
        datetime.utcnow()
        + timedelta(minutes=30)
    )

    db.commit()

    background_tasks.add_task(
        send_verification_email,
        email,
        token
    )

    return {
        "message": "Verification email sent again"
    }


# =========================
# VERIFY EMAIL
# =========================

def verify_email(
    token: str,
    db: Session
):

    user = authentication_repository.verify_email(
        db,
        token
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token"
        )

    return user


# =========================
# SKILLS
# =========================

def get_skills(db):
    return authentication_repository.get_skills(db)
def email_exist(db,email:str):
    return authentication_repository.get_user_by_email(db,email)
def send_otp(email):
    otp=secrets.randbelow(900000)+100000
    subject = "Verify your email"

    body = (
        f"Please Find The OTP For Password Reset Below:\n\n"
        f"{otp}"
    )

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL
    msg["To"] = email

    with smtplib.SMTP(
        SMTP_SERVER,
        int(SMTP_PORT)
    ) as server:

        server.starttls()

        server.login(
            SMTP_EMAIL,
           SMTP_PASSWORD
        )

        server.send_message(msg)

    return otp
def reset_password(email,new_password,db):
    return authentication_repository.reset_password(email,hash_password(new_password),db)
def update_resume_url(user_id,resume_url,resume_status,db: Session):
    return authentication_repository.update_resume_url(user_id,resume_url,resume_status,db)