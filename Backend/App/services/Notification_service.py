from models.jobs import Jobs
from repositories import users_repository
from sqlalchemy.orm import Session
from services.vector_service import VectorService
async def notifications(job_embedding :list[float],job_id):
  vector_service=VectorService()
  matching_resumes=vector_service.search_resume_vectors(job_embedding,100)
  ids=[points.id for points in matching_resumes.points if points.score>0.4]
  if ids:
    users= await users_repository.send_notification(ids,job_id)
    return users
  else:
    return []
    

  