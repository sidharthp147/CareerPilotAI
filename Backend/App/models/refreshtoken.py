from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from core.database import Base
class RefreshToken(Base):
    __tablename__="refreshtokens"
    id=Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token_hash = Column(String(100), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)