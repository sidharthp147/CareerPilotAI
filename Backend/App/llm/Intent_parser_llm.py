from openai import OpenAI
import json
from core.config import OPENAI_API_KEY, OPENAI_API_BASE,OPENAI_API_MODEL

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE,
)
async def query_llm(message:str):
    messages = [
    {
        "role": "system",
        "content": """
You are an AI query parser for a job portal.

Your task is to extract structured filters from user queries.

Return ONLY valid JSON. No explanation.

Fields:
- job_title (string or null)
- location (string or null)
- skills (array of strings or empty array)
- salary (number or null)
- experience (number in years or null)
- job_type (permanent, remote, part time, contract or null)
- apply (boolean) defaults to false
- count (number) set count to 0 if user search query doesnt contains apply or application or apply to job. 
    if user search doesnt contains any count related word and have apply or application or apply to job then set count to 1.
    if user type count value as top 5 jobs then set count to that value.
-job_ids array of int

Rules:
1. Correct spelling mistakes internally.
2. Normalize salary (e.g., "5 LPA" → 500000).
3. Extract multiple skills if present.
4. If a field is not mentioned, return null (or empty array for skills).
5. Output must be clean JSON only.
6. if the user search query contains apply or application or apply to job then set apply field to true else false. 
7. if the user search with job_ids list that job_ids 
8. if user search with multiple job_ids then set count to that value,if single set count to 1.
Example 1:
Input: "react developer jobs with 5 year experience in banglore 5 lpa full time"
Output:
{
  "job_title": "React Developer",
  "location": "Bangalore",
  "skills": ["React"],
  "salary": 500000,
  "experience": 5,
  "job_type": "permanent"
}
Example 2:
Input: "I want to apply for top  5 data analyst role with SQL and Python skills in remote jobs bangalore"
Output:
{
    "job_title": "Data Analyst",
    "location": "Bangalore",
    "skills": ["SQL", "Python"],
    "salary": null,
    "experience": null,
    "job_type": "remote",
    "apply": true,
    "count": 5
}
Example 3:
Input: " apply to remote jobs for data scientist role with python skill and 2 years experience
Output:
{
    "job_title": "Data Scientist",
    "location": null,
    "skills": ["Python"],
    "salary": null,
    "experience": 2,
    "job_type": "remote",
    "apply": true,
    "count": 1
}
"""
    },
    {"role": "user", "content": message},
]   
    response = client.chat.completions.create(
                model=OPENAI_API_MODEL,
                messages=messages,
                response_format={"type": "json_object"},
    )
    content= response.choices[0].message.content
    return json.loads(content) if content else {}
