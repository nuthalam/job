from flask import Flask, render_template, request  # Import necessary Flask modules
import requests  # Import the 'requests' library for making HTTP requests
from requests.auth import HTTPBasicAuth  # Import 'HTTPBasicAuth' from 'requests.auth'

app = Flask(__name__)  # Create a Flask application instance

API_KEY = HTTPBasicAuth('fe4c8fa7-c07c-422e-9573-4659750ab08b', '')  # Set up API authentication

@app.route("/", methods=['GET', 'POST'])  # Define a route for the root URL
def jobs():
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
            response = requests.get(api, params=data, auth=API_KEY)  # Send an API GET request

            if response.status_code == 200:  # Check if the response status code is 200 (OK)
                job_results = response.json()  # Parse the JSON response
                if "results" in job_results and job_results["results"]:
                    job_listing = job_results['results'][0]  # Get the first job listing from the results
                    title = f"Job Title: {job_listing['jobTitle']}"  # Create a job title string
                    return render_template('index.html', title=title)  # Render the template with the job title
                else:
                    return "No job listings found."  # Return a message if no job listings were found
            else:
                error_message = f"Error occurred while fetching job results. Status code: {response.status_code}"
                return render_template('index.html', error_message=error_message)
        except requests.exceptions.RequestException as e:
            error = f"An error occurred: {e}"
            return render_template('index.html', error=error)
    return render_template('index.html')  # Render the template for the initial GET request

if __name__ == "__main__":
    app.run()  # Run the Flask application if the script is executed directly