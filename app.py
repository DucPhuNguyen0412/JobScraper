from flask import Flask, render_template, request, send_file, session
import sys
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.secret_key = config['DEFAULT']['FLASK_SECRET_KEY']

sys.path.append('D:\\Job-scraper\\src')

from jobspy import scrape_jobs, JobType

@app.route('/', methods=['GET', 'POST'])
def index():
    session.pop('jobs', None)  # Clear session on reload
    
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

        # Make the URLs clickable
        jobs['job_url'] = jobs['job_url'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
        
        csv_file = 'jobs.csv'
        try:
            old_data = pd.read_csv(csv_file)
        except FileNotFoundError:
            old_data = pd.DataFrame()

        all_data = pd.concat([old_data, jobs], ignore_index=True)
        all_data.to_csv(csv_file, index=False)

        session['jobs'] = jobs.to_dict()  # Store DataFrame in session

        return render_template('index.html', tables=[jobs.to_html(classes='data', escape=False)], titles=jobs.columns.values, download_link=True)

    return render_template('index.html')

@app.route('/download')
def download():
    csv_file = 'jobs.csv'
    return send_file(csv_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
