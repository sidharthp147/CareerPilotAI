import datetime

from pydantic import BaseModel,Field
class JobRequest(BaseModel):
    title:str
    location: str
    description:str
    skills:list[str]
    job_type: str
    salary_range:str
    experience: str
class SaveJobRequest(BaseModel):
    job_id:int