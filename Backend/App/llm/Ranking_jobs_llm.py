from openai import OpenAI
import json
from core.config import OPENAI_API_KEY, OPENAI_API_BASE,OPENAI_API_MODEL

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE,
)
async def ranking_llm(joblist:dict,userlist:dict):
    messages = [
    {
        "role": "system",
        "content": """
You are an AI ranker for a job portal.

Your task is to rank the given job list based on skills,job title, location, salary, experience and job type of userlist vs joblist .

Return ONLY valid JSON. No explanation.
Sort them in descending order of semantic score.

Fields:
jobs (array of jobs)
semantic scores (array of numbers)
skill match scores (array of numbers)
location match scores (array of numbers)
final scores (array of numbers)
title match scores (array of numbers)
matched skills (array of strings)
suggessions (array of strings)

Rules:
1. Output must be clean JSON only.
2.jobs is an array of jobs after sorting based on semantic score
3.matched skills is an array of matched skills
4.suggestions is an array of suggestions for user to understands which skills are missing and what to improve to get good match for this job?
5.output should be json with single array with jobs ,matched skills and suggestions added to each job.
6.jobs must be sorted based on final score descending.
7.if semantic score is not provided then set it to 0

Example:
if llm get jobs with final score 50,75,25 , it should return jobs in descending order of final score.
as 75>50>25
"""
    }
    ]
    messages.append(
        {
            "role": "user",
            "content": json.dumps({
                "joblist":joblist,
                "userlist":userlist
            })
        }
    )
   
    response = client.chat.completions.create(
                model=OPENAI_API_MODEL,
                messages=messages,
                response_format={"type": "json_object"},
    )
    content= response.choices[0].message.content
    return json.loads(content) if content else {}
