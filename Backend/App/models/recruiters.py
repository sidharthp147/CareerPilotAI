from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from core.database import Base
class Recruiters(Base):
    __tablename__="recruiters"
    user_id=Column(Integer,ForeignKey('users.id'),primary_key=True)
    company_name=Column(String(50))
    company_description=Column(String(500))
    is_approved=Column(Boolean)
    created_at=Column(DateTime)