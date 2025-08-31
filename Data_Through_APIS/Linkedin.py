import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
  
api_key = os.getenv('SCRAPING_DOG_API_KEY')

def get_linkedin_jobs(Role, Location):

	url = "https://api.scrapingdog.com/linkedinjobs"
	
	params = {
		"api_key": api_key,
		"field": Role,
		"location": Location,
		"page":  1,
		"sort_by": "most_recent", 
	}
	
	response = requests.get(url, params=params)

	with open('Data/linkedin_jobs.json', 'w') as f:
		json.dump(response.json(), f, indent=4)
	
	if response.status_code == 200:
		data = response.json()
		print(data)
	else:
		print(f"Request failed with status code: {response.status_code}")