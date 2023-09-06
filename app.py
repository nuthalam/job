from flask import Flask, render_template, request
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

API_KEY = HTTPBasicAuth('fe4c8fa7-c07c-422e-9573-4659750ab08b', '')


@app.route("/", methods=['GET', 'POST'])
def jobs():
    if request.method == 'POST':
        location = request.form.get("location", "")
        keywords = request.form.get("keywords", "")
        full_time = request.form.get("fullTime", False)
        recruitment_agency = request.form.get("postedByRecruitmentAgency", False)
        employerId = request.form.get("employerId", "")

        api = "https://www.reed.co.uk/api/1.0/search"
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
            response = requests.get(api, params=data, auth=API_KEY)

            if response.status_code == 200:
                job_results = response.json()
                if "results" in job_results and job_results["results"]:
                    job_listing = job_results['results'][0]

                    # Extract job details
                    title = job_listing['jobTitle']
                    description = job_listing['jobDescription']
                    min_salary = job_listing['minimumSalary']
                    max_salary = job_listing['maximumSalary']

                    # Pass these details to the HTML template
                    return render_template('index.html', title=title, description=description, min_salary=min_salary, max_salary=max_salary)
                else:
                    return "No job listings found."
            else:
                error_message = f"Error occurred while fetching job results. Status code: {response.status_code}"
                return render_template('index.html', error_message=error_message)
        except requests.exceptions.RequestException as e:
            error = f"An error occurred: {e}"
            return render_template('index.html', error=error)
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run()