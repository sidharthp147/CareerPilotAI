from pydantic import BaseModel,Field
class ResendVerificationRequest(BaseModel):
    email:str
class Profile(BaseModel):
    name: str = Field(...)
    skills: str = Field(...)
    experience: str = Field(...)
    resume_url: str = Field(...)
class DashboardResponse(BaseModel):
    users: dict
    recruiters: dict
    jobs: dict
    applications: dict
    top_recruiters: list
    most_applied_jobs: list
    user_growth: list
    application_trend: list