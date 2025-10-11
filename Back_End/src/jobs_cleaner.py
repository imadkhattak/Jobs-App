# src/JobsProcessor.py

def clean_linkedin_data(linkedin):

    cleaned_jobs = []
    for job in linkedin:
        job_entry = {
            "Title": job.get("job_position", "null").replace("\n", " "),
            "Company": job.get("company_name", "null").replace("\n", " "),
            "company_profile": job.get("company_profile", "null").replace("\n", " "),
            "Location": job.get("job_location", "null").replace("\n", " "),
            "job_posting_date":job.get("job_posting_date", "null").replace("\n", " "),
            "Country": job.get("job_location", "null").split(",")[-1].strip() if job.get("job_location") else "null",
            "Job Type": job.get("job_type", "null"),   # if available
            "Salary": job.get("salary", "Not Disclosed"),       # if available
            "Link": job.get("job_link", "null"),
            "Description": job.get("job_description", job.get("job_link", "null")).replace("\n", " ")
        }
        cleaned_jobs.append(job_entry)
    return cleaned_jobs


def clean_indeed_data(indeed):

    cleaned_jobs = []
    for content in indeed.get("returnvalue", {}).get("data", []):
        job_entry = {
            "Title": content.get("title", "null"),
            "Company": content.get("companyName", "null"),
            "Location": content.get("location", {}).get("city", "null"),
            "Country": content.get("location", {}).get("country", "null") if content.get("location") else "null",
            "Job Type": content.get("jobType", "null"),
            "Salary": content.get("salary", {}).get("salaryText", "Not Disclosed"),
            "Link": content.get("jobUrl", "null"),
            "Description": content.get("descriptionText", "null")
        }
        cleaned_jobs.append(job_entry)
    return cleaned_jobs


def clean_glassdoor_data(glassdoor):

    cleaned_jobs = []
    for content in glassdoor.get("data", {}).get("jobs", []):
        salary_min = content.get('salary_min', 'N/A')
        salary_max = content.get('salary_max', 'N/A')
        salary_currency = content.get('salary_currency', '')
        job_entry = {
            "Title": content.get("job_title", "null"),
            "Company": content.get("company_name", "null"),
            "Location": content.get("location_name", "null"),
            "Country": content.get("location_name", "null").split(",")[-1].strip() if content.get("location_name") else "null",
            "Job Type": content.get("salary_period", "null"),
            "Salary": f"{salary_min} - {salary_max} {salary_currency}".strip(),
            "Link": content.get("job_link", "null"),
            "Description": ""
        }
        cleaned_jobs.append(job_entry)
    return cleaned_jobs










