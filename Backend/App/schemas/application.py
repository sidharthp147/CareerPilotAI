from pydantic import BaseModel,Field
class Applicationrequest(BaseModel):
    id:int
    job_id:int
    jobseeker_id:int
    status:str
    applied_at:str
    