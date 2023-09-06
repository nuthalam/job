# Import necessary Flask modules
from flask import Flask, render_template, request

# Import the 'requests' library for making HTTP requests
import requests

# Import 'HTTPBasicAuth' from 'requests.auth'
from requests.auth import HTTPBasicAuth

# Create a Flask application instance
app = Flask(__name__)

# Set up API authentication
API_KEY = HTTPBasicAuth('fe4c8fa7-c07c-422e-9573-4659750ab08b', '')

# Define a route for the root URL, handling both GET and POST requests
@app.route("/", methods=['GET', 'POST'])
def jobs():
    if request.method == 'POST':  # Check if the request method is POST
        location = request.form.get("location", "")  # Get the value of 'location' from the form
        keywords = request.form.get("keywords", "")  # Get the value of 'keywords' from the form
        full_time = request.form.get("fullTime", False)  # Get the value of 'fullTime' from the form
        recruitment_agency = request.form.get("postedByRecruitmentAgency", False)  # Get the value of 'postedByRecruitmentAgency' from the form
        employerId = request.form.get("employerId", "")  # Get the value of 'employerId' from the form

        # Define the API URL
        api = "https://www.reed.co.uk/api/1.0/search"

        # Create a dictionary with the parameters for the API request
        data = {
            "locationName": location,
            "temp": "True",
            "keywords": keywords,
            "fullTime": full_time,
            "postedByRecruitmentAgency": recruitment_agency,
            "distanceFromLocation": 1,
            "employerId": employerId
        }

        try:
            # Send an API GET request
            response = requests.get(api, params=data, auth=API_KEY)

            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                # Parse the JSON response
                job_results = response.json()

                if "results" in job_results and job_results["results"]:
                    # Get the first job listing from the results
                    job_listing = job_results['results'][0]

                    # Extract job details
                    title = job_listing['jobTitle']
                    location=job_listing['locationName']
                    description = job_listing['jobDescription']
                    min_salary = job_listing['minimumSalary']
                    max_salary = job_listing['maximumSalary']

                    # Pass these details to the HTML template
                    return render_template('index.html', title=title,location=location,description=description, min_salary=min_salary, max_salary=max_salary)
                else:
                    return "No job listings found."
            else:
                error_message = f"Error occurred while fetching job results. Status code: {response.status_code}"
                return render_template('index.html', error_message=error_message)
        except requests.exceptions.RequestException as e:
            error = f"An error occurred: {e}"
            return render_template('index.html', error=error)
    
    # Render the template for the initial GET request
    return render_template('index.html')


# Run the Flask application if the script is executed directly
if __name__ == "__main__":
    app.run()
