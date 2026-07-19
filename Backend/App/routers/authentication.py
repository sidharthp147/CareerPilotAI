
from fastapi import APIRouter, Depends, HTTPException, Response, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from core.database import get_db
from core.limiter import limiter
from schemas.recruiters import RecruiterRequest
from schemas.auth import LoginRequest,ForgotPasswordRequest,ResetPasswordRequest
from schemas.users import ResendVerificationRequest
from services import authentication_service
from datetime import datetime
from fastapi import UploadFile,File,Form,BackgroundTasks
from services.authentication_service import send_otp
from services import supabase_service
from models.users import Users
from fastapi.security import OAuth2PasswordRequestForm
from services import AI_service
from datetime import timedelta


SECRET = authentication_service.SECRET
ALGORITHM = authentication_service.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)
router = APIRouter(prefix="/auth", tags=["auth"])

def get_current_user(request: Request,token: str|None = Depends(oauth2_scheme),db: Session = Depends(get_db),):
    if token is None:
        return None
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="No USER")
    except JWTError:
        raise HTTPException(status_code=401, detail="ERRORed Token")
    user = authentication_service.authentication_repository.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="No USER")
    request.state.user = user
    return user
def get_current_user_optional(request: Request,token: str|None = Depends(oauth2_scheme_optional),db: Session = Depends(get_db),):
    if token is None:
        return None
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="No USER")
    except JWTError:
        raise HTTPException(status_code=401, detail="ERRORed Token")
    user = authentication_service.authentication_repository.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="No USER")
    request.state.user = user
    return user

def require_role(roles: list[str]):
    def role_check(current_user: Users = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Not Authenticated")
        return current_user
    return role_check
@router.post("/login")
@limiter.limit("50/minute")
def login(request: Request, response: Response, data: LoginRequest, db: Session = Depends(get_db)):
    result = authentication_service.login_user(data, db)
    user = result["user"]
    token = result["token"]
    refresh_token = result["refresh_token"]
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
    )
    authentication_service.save_refresh_for_user(db, user.id, refresh_token)
    return {"token": token, "success": True, "message": "Login successful", "role": user.role, "user_id": user.id}
@router.post("/registration")
@limiter.limit("25/hour")
async def registration(request: Request, background_tasks: BackgroundTasks, email: str=Form(...),password: str=Form(...),confirmpassword: str=Form(...),username: str=Form(...),skills: str=Form(...),experience: str=Form(...),file:UploadFile = File(None), db: Session = Depends(get_db)):
    resume_url=None
    resume_status=None
    response=authentication_service.register_jobseeker(background_tasks,email,password,confirmpassword,username,skills,experience,resume_url,resume_status, db, )
    user_id=authentication_service.email_exist(db,email)
    if user_id is None:
        raise HTTPException(status_code=400, detail="User not found")
    if file:
        resume_url=background_tasks.add_task(resume_upload,background_tasks,user_id.id,file=file)
        resume_status="uploading"
    return response

@router.post("/RecruiterRegister")
@limiter.limit("5/hour")
def recruiter_registration(request: Request, data: RecruiterRequest,background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return authentication_service.register_recruiter(data, db,background_tasks)

@router.post("/refresh")
def rotate_refresh_token(request: Request,response: Response,db: Session = Depends(get_db)):
    refresh_token_cookie = request.cookies.get("refresh_token")
    result = authentication_service.rotate_refresh_token(refresh_token_cookie, db)
    response.delete_cookie(key="refresh_token")
    response.set_cookie(
        key="refresh_token",
        value=result["token"],
        httponly=True,
        secure=False,#Change this to True when deploying to production because this is just for testing
        samesite="lax",
    )
    return {"token": result["access_token"], "success": True, "message": "Token refreshed successfully"}

@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token_cookie = request.cookies.get("refresh_token") 
    result = authentication_service.logout_user(refresh_token_cookie, db)
    response.delete_cookie(key="refresh_token")
    return result
@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    result = authentication_service.verify_email(token, db)
    return result
@router.post("/resend-verification")
def resend_verification(
    request: ResendVerificationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    return authentication_service.resend_verification_email(request.email,
        db, background_tasks
    )
async def resume_upload(background_tasks: BackgroundTasks,user_id :int,file:UploadFile = File(...)):
    return await supabase_service.upload_resume(background_tasks,user_id,file)
@router.get("/skills")
def get_skills(db: Session = Depends(get_db)):
    return authentication_service.get_skills(db)


@router.post("/token")
def login_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    data = LoginRequest(
        email=form_data.username,
        password=form_data.password
    )

    return authentication_service.login_user(data, db)
def resume_extract(background_tasks: BackgroundTasks,file:UploadFile = File(...)):
    return AI_service.extract_resume(background_tasks,file)
@router.post("/ForgotPassword")
@limiter.limit("25/hour")
def forgot_password(request: Request,data: ForgotPasswordRequest,db:Session= Depends(get_db)):
    user=authentication_service.email_exist(db,data.email)
    if user:
        expiry=datetime.now() + timedelta(minutes=10)
        otp=send_otp(data.email)
        return {"otp":otp,"expiry":expiry}
    raise HTTPException(status_code=404,detail="No Such Email Found")
@router.post("/resetpassword")
def password_reset(data: ResetPasswordRequest,db: Session = Depends(get_db)):
    return authentication_service.reset_password(data.email,data.new_password,db)
