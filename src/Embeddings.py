import json


with open('../Retrieved_Data/linkedin_jobs.json', 'r', encoding="utf-8") as f:
    linkedin = json.load(f)

with open('../Retrieved_Data/indeed.json', 'r', encoding="utf-8") as f:
    indeed = json.load(f)

with open('../Retrieved_Data/glassdoor.json', 'r', encoding="utf-8") as f:
    glassdoor = json.load(f)


def clean_linkedin_data(linkedin):

    for i in range(len(linkedin)):
        linkedin[i]['job_position'] = linkedin[i]['job_position'].replace('\n', ' ')
        linkedin[i]['job_link'] = linkedin[i]['job_link'].replace('\n', ' ')
        linkedin[i]['job_id'] = linkedin[i]['job_id'].replace('\n', ' ')
        linkedin[i]['company_name'] = linkedin[i]['company_name'].replace('\n', ' ')
        linkedin[i]['company_profile'] = linkedin[i]['company_profile'].replace('\n', ' ')
        linkedin[i]['job_location'] = linkedin[i]['job_location'].replace('\n', ' ')
        linkedin[i]['job_posting_date'] = linkedin[i]['job_posting_date'].replace('\n', ' ')
        linkedin[i]['company_logo_url'] = linkedin[i]['company_logo_url'].replace('\n', ' ')

    return linkedin
    

def clean_glassdoor_data(glassdoor):
    job_data = []

    for content in glassdoor['data']['jobs']:
        job_info = {
            "job_id": content.get("job_id"),
            "job_title": content.get("job_title"),
            "company_name": content.get("company_name"),
            "company_logo": content.get("company_logo"),
            "location_name": content.get("location_name"),
            "location_type": content.get("location_type"),
            "job_link": content.get("job_link"),
            "easy_apply": content.get("easy_apply"),
            "age_in_days": content.get("age_in_days"),
            "is_sponsored": content.get("is_sponsored"),
            "is_sponsored_employer": content.get("is_sponsored_employer"),
            "rating": content.get("rating"),
            "salary_currency": content.get("salary_currency"),
            "salary_period": content.get("salary_period"),
            "salary_min": content.get("salary_min"),
            "salary_median": content.get("salary_median"),
            "salary_max": content.get("salary_max"),
            "salary_source": content.get("salary_source"),
        }

        job_data.append(job_info)

    return job_data




def clean_indeed_data(indeed):
    job_data = []

    for content in indeed['returnvalue']['data']:
        job_info = {
            "jobKey": content.get("jobKey"),
            "title": content.get("title"),
            "jobType": content.get("jobType", []),
            "description": content.get("descriptionText"),
            "companyName": content.get("companyName"),
            "companyUrl": content.get("companyUrl"),
            "location": {
                "city": content.get("location", {}).get("city"),
                "postalCode": content.get("location", {}).get("postalCode"),
                "country": content.get("location", {}).get("country"),
                "countryCode": content.get("location", {}).get("countryCode"),
                "formattedAddressLong": content.get("location", {}).get("formattedAddressLong"),
                "formattedAddressShort": content.get("location", {}).get("formattedAddressShort"),
                "streetAddress": content.get("location", {}).get("streetAddress"),
                "fullAddress": content.get("location", {}).get("fullAddress"),
            },
            "salary": {
                "currency": content.get("salary", {}).get("salaryCurrency"),
                "min": content.get("salary", {}).get("salaryMin"),
                "max": content.get("salary", {}).get("salaryMax"),
                "text": content.get("salary", {}).get("salaryText"),
                "type": content.get("salary", {}).get("salaryType"),
            },
            "rating": {
                "rating": content.get("rating", {}).get("rating"),
                "count": content.get("rating", {}).get("count"),
            },
            "occupation": content.get("occupation", []),
            "attributes": content.get("attributes", []),
            "datePublished": content.get("datePublished"),
            "jobUrl": content.get("jobUrl"),
            "source": content.get("source"),
            "age": content.get("age"),
            "isRemote": content.get("isRemote"),
            "language": content.get("language"),
            "locale": content.get("locale"),
            "expired": content.get("expired"),
            "requirements": content.get("requirements", []),
            "benefits": content.get("benefits", []),
        }

        job_data.append(job_info)

    return job_data

cleaned_indeed = clean_indeed_data(indeed)
cleaned_glassdoor = clean_glassdoor_data(glassdoor)
cleaned_linkedin = clean_linkedin_data(linkedin)


all_jobs = []

# linkedin
for job in cleaned_linkedin:
    all_jobs.append({
        "id": job.get("job_id"),
        "title": job.get("job_position"),
        "company": job.get("company_name"),
        "company_profile": job.get("company_profile"),
        "job_link": job.get("job_link"),
        "location": job.get("job_location"),
        "posting_date": job.get("job_posting_date"),
        "source": "linkedin",
        "text": (
            f"{job.get('job_position')} at {job.get('company_name')} in {job.get('job_location')}. "
            f"Posted on {job.get('job_posting_date')}. "
            f"Company profile: {job.get('company_profile', '')}. "
            f"Apply here: {job.get('job_link')}"
        )
    })



for job in cleaned_glassdoor:
    all_jobs.append({
        "id": job["job_id"],
        "title": job["job_title"],
        "company": job["company_name"],
        "salary": job["salary_max"],
        "salary_period": job["salary_period"],
        "job_link": job["job_link"],
        "location": job["location_name"],
        "source": "glassdoor",
        "text": (
            f"{job['job_title']} at {job['company_name']} in {job['location_name']} "
            f"({job['location_type']}). Salary: {job['salary_max']} {job['salary_currency']} "
            f"per {job['salary_period']}. Apply here: {job['job_link']}"
        )
    })


# # indeed
# for job in cleaned_indeed:
#     all_jobs.append({
#         "id": job["jobKey"],
#         "title": job["title"],
#         "company": job["companyName"],
#         "source": "indeed",
#         "text": f"{job['title']} at {job['companyName']} in {job['location'].get('city', '')}. {job['description']}"
#     })



# print(f"Total jobs collected: {(all_jobs[0])}")

