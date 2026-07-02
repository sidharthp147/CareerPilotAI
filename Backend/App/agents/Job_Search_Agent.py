import json
from openai import OpenAI
from services.jobs_service import list_jobs
from core.config import OPENAI_API_KEY, OPENAI_API_BASE,OPENAI_API_MODEL

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE,
)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_jobs",
            "description": "Search jobs",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    },
                    "job_type": {
                        "type": "string"
                    },
                    "location": {
                        "type": "string"
                    },
                    "limit": {
                        "type": "integer"
                    },
                    "offset": {
                        "type": "integer"
                    }
                },
                "required": ["query"]
            }
        }
    },
    
]
async def run_agent(
    db,
    user_id,
    message,
    job_type,
    location,
    limit,
    offset
):

    messages = [
        {
            "role": "system",
            "content": """
You are a job portal assistant.

Rules:

1. Always call list_jobs first.

2. If the user wants to apply:
   return:

   {
      "action":"confirmation_required",
      "apply":true,
      "count":<count>
   }

3. Never apply directly.

4. Extract count:
   - apply => count=1
   - apply top 5 => count=5
   - apply top 10 => count=10
5. after recieving tool_results,respond with valid JSON only.
6.You must Never create,invent,or hallucinate jobs. You can only return jobs from tool results.
if jobs are empty then return empty jobs with total 0. Do not return any explanation or text other than valid JSON.
example Normal Search: 
return
{
    "total": <total>,
    "jobs": <jobs>},
example Apply Intent:
return  
{
    "action":"confirmation_required",
    "apply":true,
    "count":<count>
    "total": <total>,
    "jobs": <jobs>},}
Do not Include any explanation in the response. Always return valid JSON. Always call list_jobs first to get the relevant jobs based on user query. If user query contains apply or application or apply to job then set apply field to true in response and also extract count value based on user query and return in response. Never apply directly without confirmation from user.
Do not include markdown
Do not include text before or after json response


"""
        },
        {
            "role": "user",
            "content": message
        }
    ]

    response = client.chat.completions.create(
        model=OPENAI_API_MODEL,
        messages=messages,
        tools=TOOLS
    )
    tool_result=None
    while True:
        
        msg = response.choices[0].message

        if not msg.tool_calls:
            llm_response = json.loads(msg.content)
            return{
                "total": tool_result["total"] if tool_result else llm_response.get("total", 0),
                "jobs": tool_result["jobs"] if tool_result else llm_response.get("jobs", []),
                "action": llm_response.get("action"),
                "apply": llm_response.get("apply", False),
                "count": llm_response.get("count", 0)
            }

        messages.append(msg)

        for tool_call in msg.tool_calls:

            result = await list_jobs(
                db=db,
                current_user=user_id,
                search=message,
                job_type=job_type,
                location=location,
                limit=limit,
                offset=offset
            )
            tool_result=result

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        {
                            "total": result["total"],
                            "jobs": result["jobs"]
                        }
                    )
                }
            )

        response = client.chat.completions.create(
            model=OPENAI_API_MODEL,
            messages=messages,
            tools=TOOLS
        )