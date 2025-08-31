import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('INDEED_API_KEY')

def indeed_data(role):
	url = "https://indeed-scraper-api.p.rapidapi.com/api/job"

	payload = { "scraper": {
			"maxRows": 15,
			"query": role,
			"jobType": "fulltime",
			"radius": "50",
			"sort": "relevance",
			"fromDays": "7"
		} }
	headers = {
		"x-rapidapi-key": api_key,
		"x-rapidapi-host": "indeed-scraper-api.p.rapidapi.com",
		"Content-Type": "application/json"
	}

	response = requests.post(url, json=payload, headers=headers)

	with open('../Data/indeed.json', 'w', encoding="utf-8") as f:
		json.dump(response.json(), f, indent=4)

if __name__ == '__main__':
	indeed_data('AI Engineer')