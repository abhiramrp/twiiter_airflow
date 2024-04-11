import requests
import json 
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

url = "https://api.open.fec.gov/v1/candidates/" 

params = {
    "api_key": API_KEY, 
    "election_year": ["2020"],
    "per_page": "100",
    "is_active_candidate": "true",
    "office": ["P"],
    "candidate_status": ["C"]
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = json.loads(response.text)
    # print(json.dumps(data, indent=4))
    
else:
    print(response.status_code)
    print(response.text)

candidates_dict = {}

for c_dict in data["results"]:
    candid_id = c_dict["candidate_id"]
    if candid_id not in candidates_dict:
        candidates_dict[candid_id] = []
        candidates_dict[candid_id].append(c_dict["name"])
        candidates_dict[candid_id].append(c_dict["party_full"])
