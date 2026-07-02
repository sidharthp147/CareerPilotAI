from pydantic import BaseModel,Field
class RecruiterRequest(BaseModel):
    email:str
    password:str
    confirmpassword:str
    company_name:str
    company_description:str
