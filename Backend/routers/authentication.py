from passlib.context import CryptContext
from jose import jwt,JWTError
from fastapi import Depends,HTTPException,Response,Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from datetime import datetime,timedelta,timezone
from schemas import  JobseekerRegisterRequest,RecruiterRequest,LoginRequest
from models import Users,JobSeekers,Recruiters,RefreshToken
from fastapi import APIRouter
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET="632a69cf65f7e4a4174d71c14054ab2c956cf74c2f51441a540ae88a6b8fe9b3"
ALGORITHM="HS256"
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")
router=APIRouter(prefix="/auth",tags=["auth"])
def hash_password(password):
    return pwd_context.hash(password)
def hash_token(token):
    return pwd_context.hash(token)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def verify_token(plain_token, hashed_token):
    return pwd_context.verify(plain_token, hashed_token )
def create_token(data:dict,expires_minutes: int=5):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=expires_minutes)
    to_encode.update({"exp":int(expire.timestamp())})
    return jwt.encode(to_encode,SECRET,algorithm=ALGORITHM)
def create_refresh_token(data:dict,expires_days: int=7):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(days=expires_days)
    to_encode.update({"exp":int(expire.timestamp())})
    return jwt.encode(to_encode,SECRET,algorithm=ALGORITHM)
def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401,detail="No USER")

    except JWTError:
        raise HTTPException(status_code=401,detail="ERROR")

    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
     raise HTTPException(status_code=401,detail="No USER")

    return user
@router.post("/login")
def login(data:LoginRequest,response:Response,db:Session = Depends(get_db)):
    stmt = db.query(Users).filter(Users.email == data.email)
    user=stmt.first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if (user.role=="ADMIN"):
        token=create_token({"sub":str(user.id)})
        return {"token":token,"success":True,"message":"Login successful","role":user.role}
    if not verify_password(data.password,user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")
    token=create_token({"sub":str(user.id)})
    refresh_token=create_refresh_token({"sub":str(user.id)})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none"

    )
    refresh_token_hash = hash_token(refresh_token)
    db.add(RefreshToken(
        user_id=user.id,
        token_hash=refresh_token_hash,
        expires_at=datetime.now() + timedelta(minutes=60)
    ))
    db.commit()
    return {"token":token,"success":True,"message":"Login successful","role":user.role}
@router.post("/registration")
def registration(data:JobseekerRegisterRequest,db:Session = Depends(get_db)):
     if (data.password!=data.confirmpassword):
        raise HTTPException(status_code=400, detail="Password Doesn't Match")
     else:
        reg_model1=Users(
        email=data.email,
        password_hash=hash_password(data.password),
        role="USER",
        is_active=True,
        created_at=datetime.now())
        db.add(reg_model1)
        db.commit()
        db.refresh(reg_model1)
        reg_model2=JobSeekers(user_id=reg_model1.id,
                              name=data.username,
                              skills=data.skills,
                              experience=data.experience,
                              resume_url=data.resume_url)
        db.add(reg_model2)
        db.commit()
        return {"message","Registration Successful"}
@router.post("/RecruiterRegister")
def registration(data:RecruiterRequest,db:Session = Depends(get_db)):
     if (data.password!=data.confirmpassword):
        raise HTTPException(status_code=400, detail="Password Doesn't Match")
     else:
        reg_model1=Users(
        email=data.email,
        password_hash=hash_password(data.password),
        role="RECRUITER",
        is_active=True,
        created_at=datetime.now())
        db.add(reg_model1)
        db.commit()
        db.refresh(reg_model1)
        reg_model2=Recruiters(user_id=reg_model1.id,
                             company_name=data.company_name,
                             company_description=data.company_description,
                             is_approved=False)
        db.add(reg_model2)
        db.commit()
        return {"message":"Registration Successful"}
@router.post("/refresh")
def refresh_token(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = jwt.decode(refresh_token, SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    token_hash = hash_token(refresh_token)
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash,
        RefreshToken.is_revoked == False
    ).first()

    if not db_token:
        raise HTTPException(status_code=401, detail="Refresh token revoked")
    token = create_token({"sub": user_id})
    payload=jwt.decode(refresh_token, SECRET, algorithms=[ALGORITHM])
    exp_timestamp = payload.get("exp")

    if not exp_timestamp:
        db_token.is_revoked = True
        db.commit()
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    now = datetime.now(timezone.utc)
    if exp_datetime < now:
        db_token.is_revoked = True
        db.commit()
        raise HTTPException(status_code=401, detail="Refresh token expired")

        
    return {
        "token": token
    }
@router.get("/logout")
def logout(request:Request,response:Response,db:Session=Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")   
    if not verify_token(refresh_token, hash_token(refresh_token)):
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    res=db.query(RefreshToken).filter(RefreshToken.is_revoked==False).first()
    if res:
        res.is_revoked=True
        db.commit()
        response.delete_cookie(
        key="refresh_token"
        )
    return {"message":"Logged out successfully"}
     