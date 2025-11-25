import os
import json
import ollama
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage


# Stage 1: Explain matching jobs
def explain_matching_jobs(cv_info, all_jobs):
    """
    Match CV to jobs and return top 15 most relevant jobs.
    Uses structured reasoning through Ollama for scoring and comparison.
    """
    jobs_text = "\n\n".join([json.dumps(job, indent=2) for job in all_jobs])

    prompt = PromptTemplate(
        input_variables=["cv_info", "jobs"],
        template=(
            "You are an AI career coach that ONLY outputs valid JSON.\n\n"
            "Candidate Profile:\n{cv_info}\n\n"
            "Job Postings:\n{jobs}\n\n"
            "Task:\n"
            "- Identify the top 15 most relevant jobs for this candidate.\n"
            "- Compare job descriptions with candidate skills and projects.\n"
            "- Return ONLY a valid JSON array with this EXACT structure:\n\n"
            "[\n"
            "  {{\n"
            '    "Job Title": "string",\n'
            '    "Company": "string",\n'
            '    "Relevance Score": 85,\n'
            '    "Missing Skills": ["skill1", "skill2"],\n'
            '    "Link": "string",\n'
            '    "Salary": "string"\n'
            "  }}\n"
            "]\n\n"
            "CRITICAL RULES:\n"
            "- Use DOUBLE QUOTES for all keys and string values\n"
            "- NO markdown, NO explanations, NO text before or after the JSON\n"
            "- Start with [ and end with ]\n"
            "- Relevance Score must be a number between 0-100\n"
            "- Missing Skills must be an array (use [] if no missing skills)\n"
        )
    )

    
    final_prompt = prompt.format(
        cv_info=json.dumps(cv_info, indent=2),
        jobs=jobs_text
    )

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": "You are a JSON-only AI job matching system."},
            {"role": "user", "content": final_prompt},
        ],
    )

    raw = response["message"]["content"].strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print("⚠️ LLM returned invalid JSON. Attempting recovery...")
        start = raw.find("[")
        end = raw.rfind("]")
        if start != -1 and end != -1:
            try:
                return json.loads(raw[start:end+1])
            except:
                pass
        print(f"LLM output that failed to parse:\n{raw}")
        raise ValueError("LLM returned invalid JSON that could not be recovered.")

