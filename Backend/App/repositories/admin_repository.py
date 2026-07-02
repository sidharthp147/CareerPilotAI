from sqlalchemy.orm import Session
from sqlalchemy import func
from models.users import JobSeekers
from models.recruiters import Recruiters
from models.jobs import Jobs
from models.application import Applications
from models.users import Users
from datetime import datetime, timedelta
def get_analytics(db: Session) :
    users = get_period_counts(
        db.query(Users).filter((Users.role != "ADMIN")),
        Users.created_at
    )

    recruiters = get_period_counts(
        db.query(Recruiters),
        Recruiters.created_at
    )

    jobs = get_period_counts(
        db.query(Jobs),
        Jobs.created_at
    )

    applications = get_period_counts(
        db.query(Applications),
        Applications.applied_at
    )

    # Top recruiters by jobs posted

    top_recruiters = (
        db.query(
            Recruiters.company_name,
            func.count(Jobs.id).label("jobs")
        )
        .join(
            Jobs,
            Recruiters.user_id == Jobs.recruiter_id
        )
        .group_by(
            Recruiters.company_name
        )
        .order_by(
            func.count(Jobs.id).desc()
        )
        .limit(5)
        .all()
    )

    top_recruiters = [
        {
            "name": r.company_name,
            "jobs": r.jobs
        }
        for r in top_recruiters
    ]

    # Most applied jobs

    most_applied_jobs = (
        db.query(
            Jobs.heading,
            func.count(
                Applications.id
            ).label("applications")
        )
        .join(
            Applications,
            Jobs.id == Applications.job_id
        )
        .group_by(
            Jobs.heading
        )
        .order_by(
            func.count(
                Applications.id
            ).desc()
        )
        .limit(5)
        .all()
    )

    most_applied_jobs = [
        {
            "title": j.heading,
            "applications": j.applications
        }
        for j in most_applied_jobs
    ]

    # User growth chart

    user_growth = (
        db.query(
            func.date_format(
                Users.created_at,
                "%Y-%m"
            ).label("month"),
            func.count(
                Users.id
            ).label("count")
        ).filter(Users.role != "ADMIN")
        .group_by("month")
        .order_by("month")
        .all()
    )

    user_growth = [
        {
            "month": x.month,
            "count": x.count
        }
        for x in user_growth
    ]

    # Application trend chart

    application_trend = (
        db.query(
            func.date_format(
                Applications.applied_at,
                "%Y-%m"
            ).label("month"),
            func.count(
                Applications.id
            ).label("count")
        )
        .group_by("month")
        .order_by("month")
        .all()
    )

    application_trend = [
        {
            "month": x.month,
            "count": x.count
        }
        for x in application_trend
    ]

    return {
        "users": users,
        "recruiters": recruiters,
        "jobs": jobs,
        "applications": applications,
        "top_recruiters": top_recruiters,
        "most_applied_jobs": most_applied_jobs,
        "user_growth": user_growth,
        "application_trend": application_trend
    }
def get_pending_recruiters(db: Session):
    return db.query(Recruiters).filter(Recruiters.is_approved.is_(False)).all()
def get_recruiter_by_user_id(db: Session, user_id: int) -> Recruiters | None:
    return db.query(Recruiters).filter(Recruiters.user_id == user_id).first()
def set_recruiter_approved(db: Session, recruiter: Recruiters, approved: bool | None):
    recruiter.is_approved = approved
    db.commit()
    db.refresh(recruiter)
    return recruiter
def set_recruiter_rejected(db: Session, recruiter: Recruiters, rejected: bool | None):
    recruiter.is_approved = rejected
    db.commit()
    db.refresh(recruiter)
    return recruiter

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