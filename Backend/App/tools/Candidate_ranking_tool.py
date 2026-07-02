from services.vector_service import VectorService
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from repositories import users_repository
from llm.Candidate_Ranking_llm import candidate_ranking_llm
from models.users import ResumeData
from sentence_transformers import SentenceTransformer
model=SentenceTransformer('all-MiniLM-L6-v2')
from sentence_transformers.util import cos_sim
def rank_candidates_tool(db,job, applications):
  vector_service=VectorService()
  ranked = []
  job_vector=vector_service.get_job_vector(job.id)
  if not job_vector:
      return None
  job_vec=np.array(job_vector.vector).reshape(1,-1)
  for app in applications:
      resume_vector = vector_service.get_resume_vector(
          app["job_seeker_id"]
      )
      
      if not resume_vector:
          continue
      resume_vec=np.array(resume_vector.vector).reshape(1,-1)
      data=vector_service.get_resume_data(app["job_seeker_id"])
      user_skills=data["skills"] if data["skills"] else ""
      user_skills=",".join(user_skills)
      user_role=data["job_role"] if data["job_role"] else ""
      user_experience=int(data["experience"]) if data["experience"] else 0
      skills_score=float(cos_sim(model.encode(user_skills,convert_to_tensor=True),model.encode(job.skills,convert_to_tensor=True)))
      role_score=float(cos_sim(model.encode(user_role,convert_to_tensor=True),model.encode(job.heading,convert_to_tensor=True)))
      experience_score=float(cos_sim(model.encode(str(user_experience),convert_to_tensor=True),model.encode(str(job.experience),convert_to_tensor=True)))
      score = cosine_similarity(
          job_vec,
          resume_vec
      )[0][0]
      score_final = (score*4 + skills_score*4 + role_score*2 + experience_score*2)/10
      resume_data=users_repository.get_resume_data(app["job_seeker_id"])
      ranked.append({
          "candidate": app,
          "resume": resume_data,
          "similarity": score_final,
      })

  ranked.sort(
      key=lambda x: x["similarity"],
      reverse=True
  )
  llm_ranking=candidate_ranking_llm(job,ranked)
  return llm_ranking