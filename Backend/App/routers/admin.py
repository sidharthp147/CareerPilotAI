from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from routers.authentication import require_role
from services import admin_service
import json
from core.redis import redis_client as redis

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_role(["ADMIN"]))],
    
)
@router.get("/AdminAnalytics")
async def admin_analytics(db: Session = Depends(get_db)):
    cache_key=f"admin_analytics"
    cached_data=await redis.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    response= admin_service.get_analytics(db)
    await redis.setex(cache_key, 300, json.dumps(response))
    return response
@router.get("/recruiters")
def fetch_recruiters(db: Session = Depends(get_db)):
    return admin_service.list_pending_recruiters(db)
@router.post("/{id}/approve")
def approve_recruiter(id: int, db: Session = Depends(get_db)):
    return admin_service.approve_recruiter(db, id)
@router.post("/{id}/reject")
def reject_recruiter(id: int, db: Session = Depends(get_db)):
    return admin_service.reject_recruiter(db, id)
from datetime import datetime, timedelta

def get_period_counts(query, column):
    now = datetime.utcnow()

    today = now.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    week = today - timedelta(days=today.weekday())

    month = today.replace(day=1)

    year = today.replace(
        month=1,
        day=1
    )

    return {
        "today": query.filter(column >= today).count(),
        "week": query.filter(column >= week).count(),
        "month": query.filter(column >= month).count(),
        "year": query.filter(column >= year).count(),
        "total": query.count()
    }