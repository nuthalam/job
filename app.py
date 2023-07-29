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
        "fullTime": "False",
        "distanceFromLocation": 1,
        "keywords": "chef",
        "employerId": 365740

    }
    response = requests.get(api, params=data, auth=Key)
    return response.json()
    if response.status_code == 200:
            job_results = response.json()
            if "results" in job_results and len(job_results["results"]) > 0:
                # Display the first job listing in the results
                job_listing = job_results['results'][0]
                return f"Job Title: {job_listing['jobTitle']}"
            else:
                return "No job listings found."
    else:
            return f"Error occurred while fetching job results. Status code: {response.status_code}"