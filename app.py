from flask import Flask, render_template, request
import sys
sys.path.append('D:\\Job-scraper\\src')

from jobspy import scrape_jobs, JobType  # make sure to import JobType as well
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        location = request.form['location']
        distance = int(request.form['distance']) if request.form['distance'] else None
        job_type = JobType[request.form['job_type'].upper().replace(' ', '_')] if request.form['job_type'] else None
        results_wanted = int(request.form['results_wanted']) if request.form['results_wanted'] else 10

        jobs = scrape_jobs(
            site_name=["indeed", "linkedin", "zip_recruiter"],
            search_term=search_term,
            location=location,
            distance=distance,
            job_type=job_type,
            results_wanted=results_wanted
        )
        
        if jobs.empty:
            return render_template('index.html', message="No jobs found.")
        
        return render_template('index.html', tables=[jobs.to_html(classes='data')], titles=jobs.columns.values)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
