from flask import Flask, render_template, request  # Import necessary Flask modules
import requests  # Import the 'requests' library for making HTTP requests
from requests.auth import HTTPBasicAuth  # Import 'HTTPBasicAuth' from 'requests.auth'

app = Flask(_name_)  # Create a Flask application instance

Key = HTTPBasicAuth('2e03f95f-cf38-4bf9-b8c3-4ce1aa1bce41', '')# Set up API authentication
@app.route("/", methods=['GET', 'POST'])  # Define a route for the root URL

def reed():
    if request.method == 'POST':  # Check if the request method is POST
        location = request.form.get("location", "")  # Get the value of 'location' from the form
        keywords = request.form.get("keywords", "")  # Get the value of 'keywords' from the form
        full_time = request.form.get("fullTime", False)  # Get the value of 'fullTime' from the form
        recruitment_agency = request.form.get("postedByRecruitmentAgency", False)  # Get the value of 'postedByRecruitmentAgency' from the form
        employerId = request.form.get("employerId", "")  # Get the value of 'employerId' from the form
    api = "https://www.reed.co.uk/api/1.0/search"  # Define the API URL
    data = {
        "locationName": location,
            "temp": "True",
            "keywords": keywords,
            "fullTime": full_time,
            "postedByRecruitmentAgency": recruitment_agency,
            "distanceFromLocation": 1,
            "employerId": employerId
        }  # Create a dictionary with the parameters for the API request
    try:
        response = requests.get(api, params=data, auth=Key)# Send an API GET request

        # Check if the API request was successful (HTTP status code 200)
        if response.status_code == 200:# Check if the response status code is 200 (OK)
            job_results = response.json()# Parse the JSON response
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

