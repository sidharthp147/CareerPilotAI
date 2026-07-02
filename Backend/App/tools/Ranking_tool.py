from sentence_transformers import SentenceTransformer
model=SentenceTransformer('all-MiniLM-L6-v2')
import numpy as np
from sentence_transformers.util import cos_sim
def get_embedding(text):
    return model.encode(text).tolist()
async def rank_jobs(joblist:dict,userlist:dict):
    user_skills = userlist["user_skills"] or ""
    user_title = userlist["user_title"] or ""
    user_location = userlist["user_location"] or ""
    count=0
    for job in joblist:
            count+=1
            semantic_score = job["semantic_score"] if "semantic_score" in job else 0
            
            skills_score = calculate_skill_match(
                user_skills,
                job["skills"]
            )

            title_score = calculate_title_match(
                user_title,
                job["heading"]
            )
            if user_location=="":
                location_score=0.5
            else:
                location_score = calculate_location_match(
                user_location,
                job["location"]
            )
            final_score = (
                semantic_score * 0.3 +
                skills_score * 0.4 +
                title_score * 0.2 +
                location_score * 0.1
            )

            job["final_score"] = final_score
            job["semantic_score"] = semantic_score
            job["skills_score"] = skills_score
            job["title_score"] = title_score
            job["location_score"] = location_score

    return {"total": count, "jobs": joblist}
def calculate_skill_match(user_skills, job_skills):
    if isinstance(user_skills, list):
        user_skills = ",".join(user_skills)
    if isinstance(job_skills, list):
        job_skills = ",".join(job_skills)
    score=float(cos_sim(model.encode(user_skills,convert_to_tensor=True),model.encode(job_skills,convert_to_tensor=True)))


    return round(score, 2)
    
def calculate_title_match(user_title, job_title):
    if not user_title or not job_title:
        return 0

    # Normalize
    user_words = {word.strip().lower() for word in user_title.split()}
    job_title = {word.strip().lower() for word in job_title.split()}
    matched_title = user_words.intersection(job_title)
    score= len(matched_title) / len(user_words)

    return round(score, 2)
def calculate_location_match(user_location, job_location):
    if not user_location or not job_location:
        return 0

    # Normalize
    user_location = {word.strip().lower() for word in user_location.split()}
    job_location = {word.strip().lower() for word in job_location.split()}

    matched_location = user_location.intersection(job_location)
    score = len(matched_location) / len(user_location) if user_location else 0

    return round(score, 2)