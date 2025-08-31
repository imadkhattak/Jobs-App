import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GLASSDOOR_API_KEY')


def glassdoor_data(Role):

    url = "https://real-time-glassdoor-data.p.rapidapi.com/job-search"

    querystring = {"query":Role,"location":"new york","location_type":"ANY","min_company_rating":"ANY"}

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "real-time-glassdoor-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    with open('../Data/glassdoor.json', 'w', encoding="utf-8") as f:
        json.dump(response.json(), f, indent=4)

if __name__ == "__main__":

    glassdoor_data("AI Engineer")