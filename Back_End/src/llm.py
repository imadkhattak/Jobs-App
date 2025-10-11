# src/processing/LLM.py

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
            "You are an AI career coach.\n\n"
            "Candidate Profile:\n{cv_info}\n\n"
            "Job Postings:\n{jobs}\n\n"
            "Task:\n"
            "- Identify the top 15 most relevant jobs for this candidate.\n"
            "- Compare job descriptions with candidate skills and projects.\n"
            "- Return only JSON with this schema:\n"
            "[\n"
            "  {{\n"
            "    'Job Title': str,\n"
            "    'Company': str,\n"
            "    'Relevance Score': int (0–100),\n"
            "    'Missing Skills': [str],\n"
            "    'Link': str,\n"
            "    'Salary': str\n"
            "  }}\n"
            "]\n"
            "No markdown, explanations, or prose — only valid JSON."
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
        return {"raw_output": raw}

