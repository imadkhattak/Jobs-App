# Local imports
import os
import json
from .cv_parser import extract_text
from .llm import explain_matching_jobs

from .jobs_cleaner import (
    clean_indeed_data,
    clean_linkedin_data,
    clean_glassdoor_data
)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute paths to the data files
linkedin_path = os.path.join(script_dir, "..", "data", "retrieved_data", "linkedin_jobs.json")
indeed_path = os.path.join(script_dir, "..",  "data", "retrieved_data", "indeed.json")
glassdoor_path = os.path.join(script_dir, "..", "data", "retrieved_data", "glassdoor.json")

with open(linkedin_path, "r", encoding="utf-8") as f:
    linkedin_data = json.load(f)

with open(indeed_path, "r", encoding="utf-8") as f:
    indeed_data = json.load(f)

with open(glassdoor_path, "r", encoding="utf-8") as f:
    glassdoor_data = json.load(f)


# Clean all datasets
cleaned_indeed = clean_indeed_data(indeed_data)
cleaned_linkedin = clean_linkedin_data(linkedin_data)
cleaned_glassdoor = clean_glassdoor_data(glassdoor_data)

# Combine all cleaned jobs into one list
all_jobs = cleaned_indeed + cleaned_linkedin + cleaned_glassdoor



if __name__ == "__main__":
    cv_content = extract_text(r"../data/cvs/imad ud din khattak.pdf")
    result = explain_matching_jobs(cv_content, all_jobs)

    print("\n=== Top Matching Jobs ===\n")
    print(json.dumps(result, indent=2))

