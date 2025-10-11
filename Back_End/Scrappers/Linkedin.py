# src/Jobs_Scrapper/Linkedin.py

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
  
api_key = os.getenv('SCRAPING_DOG_API_KEY')

def get_linkedin_jobs(Role):

	url = "https://api.scrapingdog.com/linkedinjobs"
	
	params = {
		"api_key": api_key,
		"field": Role,
		"page":  1,
		"sort_by": "most_recent", 
	}
	
	response = requests.get(url, params=params)

	with open('../../Retrieved_Data/linkedin_jobs.json', 'w', encoding="utf-8") as f:
		json.dump(response.json(), f, indent=4)
	
