from flask import Flask, render_template, request  # Import necessary Flask modules
import requests  # Import the 'requests' library for making HTTP requests
from requests.auth import HTTPBasicAuth  # Import 'HTTPBasicAuth' from 'requests.auth'

app = Flask(_name_)  # Create a Flask application instance

Key = HTTPBasicAuth('2e03f95f-cf38-4bf9-b8c3-4ce1aa1bce41', '')# Set up API authentication
@app.route("/", methods=['GET', 'POST'])  # Define a route for the root URL

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
    try:
        response = requests.get(api, params=data, auth=Key)

        # Check if the API request was successful (HTTP status code 200)
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

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

