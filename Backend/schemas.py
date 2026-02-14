from pydantic import BaseModel,Field
class LoginRequest(BaseModel):
    email:str
    password:str
class JobseekerRegisterRequest(BaseModel):
    email:str
    password:str
    confirmpassword:str
    username:str
    skills:str
    experience:float
    resume_url:str
class RecruiterRequest(BaseModel):
    email:str
    password:str
    confirmpassword:str
    company_name:str
    company_description:str

class JobRequest(BaseModel):
    title:str
    location: str
    description:str
    skills:str
    job_type: str
    salary_range:str








