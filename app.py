from flask import Flask
import requests
from requests.auth import HTTPBasicAuth

Key = HTTPBasicAuth('2e03f95f-cf38-4bf9-b8c3-4ce1aa1bce41', '')
app = Flask('Flask')

@app.route("/")
def reed():
    api = "https://www.reed.co.uk/api/1.0/search"
    data = {
        "locationName": "London",
        "temp": "false",
        "postedByRecruitmentAgency": "True",
        "distanceFromLocation": 1,
        "keywords": "chef"
    }
    response = requests.get(api, params=data, auth=Key)
    return response.json()