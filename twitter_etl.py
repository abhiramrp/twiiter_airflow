
import pandas as pd
import json 
from datetime import datetime
import s3fs
import os
from dotenv import load_dotenv

import requests
import json 

from candidate_data import candidates_dict

load_dotenv()

API_KEY = os.getenv('API_KEY')

url = "https://api.open.fec.gov/v1/presidential/contributions/by_candidate/" 

contribution_list = []

def collect_data(page_num):

    params = {
        "api_key": API_KEY, 
        "election_year": ["2020"],
        "page": str(page_num), 
        "per_page": "90"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = json.loads(response.text)
        # print(json.dumps(data, indent=4)) 
    else:
        return
        print(response.status_code)
        print(response.text)



    for c_dict in data["results"]:

        candid_id = c_dict["candidate_id"]

        if candid_id not in candidates_dict:
            continue

        candidate_info = candidates_dict[candid_id]

        refined_contribution = {
            "candidate_id": candid_id,
            "name": candidate_info[0],
            "party": candidate_info[1],
            "net_receipts": c_dict["net_receipts"],
            "rounded_net_receipts": c_dict["rounded_net_receipts"]
        }

        contribution_list.append(refined_contribution)



for i in range(1, 10):
    collect_data(i)


df = pd.DataFrame(contribution_list)
df.to_csv('contribution_data.csv')