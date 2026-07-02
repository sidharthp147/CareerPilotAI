from repositories import jobs_repository
from fastapi import Depends
from core.database import get_db
from sqlalchemy.orm import Session
from repositories import  jobs_repository
from services.vector_service import VectorService
from sentence_transformers import SentenceTransformer
model=SentenceTransformer('all-MiniLM-L6-v2')
from llm.Intent_parser_llm import query_llm
import hashlib
from core.redis import redis_client as redis
from services.vector_service import VectorService
from datetime import datetime
async def search_tool(search : str ,job_type : str ,location : str ,limit : int ,offset : int ,db: Session):
  response=await query_llm(search)
  wants_apply=response.get("apply") if "apply" in response else False
  count=response.get("count") if "count" in response else 0
  search=response.get("job_title") if response.get("job_title") else ""
  skills=response.get("skills") if response.get("skills") else ""
  location=response.get("location") if response.get("location") else ""
  job_type=response.get("job_type") if response.get("job_type") else ""
  experience=response.get("experience") if response.get("experience") else ""
  job_ids=response.get("job_ids") if response.get("job_ids") else ""
  if job_ids:
    response= jobs_repository.list_job_ids(job_ids,job_type,location, 50, 0,db)
    return{"jobs":response.get("jobs"), "total":response.get("total"), "apply":wants_apply, "count":count}
  db_response= await jobs_repository.list_jobs(None, search, job_type,skills,None,experience,location,limit,offset,db)
  jobs_db=db_response.get("jobs") if db_response else []
  embedding=get_embedding(search)
  vector_service=VectorService()
  result=vector_service.search_vectors(embedding,50)
  score_map={points.id:points.score for points in result.points if points.score>0.25}
  ids=[points.id for points in result.points if points.score>0.25]
  if ids:
    response= await jobs_repository.list_jobs(ids, None, None,None,None,None, None, 50, 0,db)
    jobs_vectors=response.get("jobs")
    for job in jobs_vectors:
      job["semantic_score"]=score_map[job["id"]]
    jobs_set={}
    for job in jobs_db:
      jobs_set[job["id"]]=job
    if ids:
      for job in jobs_vectors:
        if job["id"] in jobs_set:
           jobs_set[job["id"]]["semantic_score"]=job["semantic_score"]
           continue
        else:
          jobs_set[job["id"]]=job
      jobs=list(jobs_set.values())
      total=len(jobs)
      return {"jobs":jobs,"total":total,"apply": wants_apply,"count": count,"location":location,"job_type":job_type}
  total=len(jobs_db)
  return {"jobs":jobs_db,"total":total,"apply": wants_apply,"count": count,"location":location,"job_type":job_type}

def get_embedding(text: str) -> list[float]:
    return model.encode(text).tolist()