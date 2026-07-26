import json
import os
from openai import OpenAI
from job_hunter.config.settings import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL

# Load keywords
with open(os.path.join(os.path.dirname(__file__), "..", "config", "keywords.json"), 'r') as f:
    RESUME_KEYWORDS = json.load(f)

def process_job_with_llm(job_data):
    """
    Uses OpenAI (or compatible API) to score the job against resume keywords.
    Returns a dict with: ai_score, ai_summary, key_skills
    """
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_or_groq_api_key":
        print("[!] No valid OpenAI API key found. Using mock LLM response.")
        # Fallback if no key is provided, just basic string matching
        score = 50
        if "vapt" in job_data['description'].lower(): score += 30
        return {
            "ai_score": score,
            "ai_summary": "Mock summary due to missing API key.",
            "key_skills": "Mock, Skills"
        }

    try:
        client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )

        prompt = f"""
        You are an expert tech recruiter evaluating a job description against a candidate's resume keywords.
        Candidate's Keywords: {json.dumps(RESUME_KEYWORDS)}
        
        Job Title: {job_data.get('title')}
        Job Description: {job_data.get('description')}
        
        Evaluate the job and return ONLY a valid JSON object with the following keys:
        - ai_score: An integer from 1 to 100 representing how well the job matches the candidate's keywords.
        - ai_summary: A 2-3 sentence summary of the role.
        - key_skills: A comma-separated string of the technical skills extracted from the job description.
        """

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        result = json.loads(content)
        return {
            "ai_score": result.get("ai_score", 0),
            "ai_summary": result.get("ai_summary", ""),
            "key_skills": result.get("key_skills", "")
        }

    except Exception as e:
        print(f"[-] LLM Error: {e}")
        return {
            "ai_score": 0,
            "ai_summary": f"Error processing: {e}",
            "key_skills": ""
        }
