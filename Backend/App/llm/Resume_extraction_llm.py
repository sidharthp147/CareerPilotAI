import requests
from openai import OpenAI
import json
from fastapi import Query, HTTPException
from fastapi import BackgroundTasks
from fastapi import HTTPException,File
import fitz  # PyMuPDF
import re
from services.vector_service import VectorService 
from repositories import users_repository
from services.jobs_service import get_embedding
from core.config import OPENAI_API_KEY, OPENAI_API_BASE,OPENAI_API_MODEL
from core.logging import setup_logging
import logging

setup_logging() 
logger=logging.getLogger(__name__)



client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE,
)
async def resume_extraction(file_url:str,user_id:int):
   response=requests.get(file_url,timeout=20)
   if response.status_code!=200:
    raise HTTPException(status_code=400,detail="Unable to fetch the resume from the provided URL.")
   pdf=fitz.open(stream=response.content, filetype="pdf")
   text=""
   for page in pdf:
    text+=page.get_text()
   text=re.sub(r'\s+', ' ', text)
   messages= [
   {
    "role": "system",
    "content": """
    You are an AI resume parser.

    Extract structured resume data.
    role is users 

    Return ONLY valid JSON.

    Fields:
    - full_name
    -job_role
    - email
    - phone
    - skills
    - experience
    -years of experience
    - education
    - projects
    - certifications
    - linkedin
    - github
    - summary

    """
    }, {
    "role": "user",

    "content": text
    }
    ]
   response = client.chat.completions.create(
    model=OPENAI_API_MODEL,
    messages=messages,
    response_format={"type": "json_object"},
    )
   content= response.choices[0].message.content
   if content is None:
    raise HTTPException(status_code=400,detail="Unable to extract resume data from the provided resume.")
   try:
    text1=f"""
    Full_Name:{json.loads(content)["full_name"]}
    Job_Role:{json.loads(content)["job_role"]}
    Email:{json.loads(content)["email"]}
    Phone:{json.loads(content)["phone"]}
    Skills:{json.loads(content)["skills"]}
    Experience:{json.loads(content)["years_of_experience"]}
    Education:{json.loads(content)["education"]}
    Projects:{json.loads(content)["projects"]}
    Certifications:{json.loads(content)["certifications"]}
    LinkedIn:{json.loads(content)["linkedin"]}
    GitHub:{json.loads(content)["github"]}
    Summary:{json.loads(content)["summary"]}
    """
    text2=f"""
    Job_Role:{json.loads(content)["job_role"]}
    Skills:{json.loads(content)["skills"]}
    Experience:{json.loads(content)["years_of_experience"]}
    """
    vector_service=VectorService()
    embedding1=get_embedding(text1)
    embedding2=get_embedding(text2)
    vector_service.remove_resume_embedding(user_id=user_id)
    vector_service.remove_recommendations(user_id=user_id)
    vector_service.store_resume_embedding(user_id=user_id,embedding=embedding1,job_role=json.loads(content)["job_role"],skills=json.loads(content)["skills"],years_of_experience=json.loads(content)["years_of_experience"])
    vector_service.store_recommendations(user_id=user_id,embedding=embedding2)
   except Exception as e:
    logger.error(e)
   try:
    users_repository.resume_data(user_id,resume_data=json.loads(content))
   except Exception as e:
    logger.error(e)

