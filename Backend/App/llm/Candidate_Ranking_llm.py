from openai import OpenAI
from core.config import OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_API_MODEL

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE,
)
def candidate_ranking_llm(job :list,ranked :dict):
    for ranked_data in ranked:
      resume=ranked_data["resume"]
      prompt=f"""You are a recruiter assistant.

          Job Title:
          {job.heading}

          Required Skills:
          {job.skills}

          Job Description:
          {job.description}

          Candidate Role:
          {resume.role}

          Candidate Skills:
          {resume.skills}

          Candidate Experience:
          {resume.experience}

          Similarity Score:
          {round(ranked_data["similarity"] * 100, 2)}%

          Explain in 2-3 sentences why this candidate was ranked for this job.
          Focus on:
          1. Skill match
          2. Experience relevance
          3. Job-role alignment

          Keep response under 80 words."""
      response = client.chat.completions.create(
          model=OPENAI_API_MODEL,
          messages=[
            {
                "role": "system",
                "content": "You are an expert recruiter."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

      ranked_data["explanation"] = response.choices[0].message.content

    return ranked
      