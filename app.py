from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import configparser
import sys

# Initialize Config and Flask
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.secret_key = config['DEFAULT']['FLASK_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config['DEFAULT']['DB_URL']

db = SQLAlchemy(app)

# Include job scraper
sys.path.append('D:\\Job-scraper\\src')
from jobspy import scrape_jobs, JobType

class JobSearch(db.Model):
    search_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_term = db.Column(db.String(255))
    location = db.Column(db.String(255))
    distance = db.Column(db.Integer)
    job_type = db.Column(db.String(50))
    results_wanted = db.Column(db.Integer)


class JobResult(db.Model):
    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_id = db.Column(db.Integer, db.ForeignKey('job_search.search_id'))
    site = db.Column(db.String(50))
    title = db.Column(db.String(255))
    company_name = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    job_type = db.Column(db.String(50))
    interval = db.Column(db.String(50))
    min_amount = db.Column(db.Float)
    max_amount = db.Column(db.Float)
    job_url = db.Column(db.Text)
    description = db.Column(db.Text)


@app.route('/', methods=['GET', 'POST'])
def index():
    jobs = None  # Initialize jobs to None
    titles = None  # Initialize titles to None
    no_results = False  # Initialize no_results flag
    
    if request.method == 'POST':
        try:
            search_term = request.form['search_term']
            location = request.form['location']
            distance = int(request.form['distance']) if request.form['distance'] else None
            job_type = JobType[request.form['job_type'].upper().replace(' ', '_')] if request.form['job_type'] else None
            results_wanted = int(request.form['results_wanted']) if request.form['results_wanted'] else 10

            # Perform the job search
            jobs = scrape_jobs(
                site_name=["indeed", "linkedin", "zip_recruiter"],
                search_term=search_term,
                location=location,
                distance=distance,
                job_type=job_type,
                results_wanted=results_wanted
            )
            
            if not jobs.empty:
                jobs['job_url'] = jobs['job_url'].apply(lambda x: f'<a href="{x}" target="_blank">Link</a>')

            if jobs.empty:
                no_results = True
                return render_template('index.html', message="No jobs found.")
            
            # Save search to DB
            new_search = JobSearch(
                search_term=search_term,
                location=location,
                distance=distance,
                job_type=job_type,
                results_wanted=results_wanted
            )
            db.session.add(new_search)
            db.session.commit()
            
            # Save job results to DB
            for index, row in jobs.iterrows():
                new_result = JobResult(
                    search_id=new_search.search_id,
                    site=row['site'],
                    title=row['title'],
                    company_name=row['company_name'],
                    city=row['city'],
                    state=row['state'],
                    job_type=row['job_type'],
                    interval=row['interval'],
                    min_amount=row['min_amount'],
                    max_amount=row['max_amount'],
                    job_url=row['job_url'],
                    description=row['description']
                )
                db.session.add(new_result)

            db.session.commit()

            titles = jobs.columns.values
            
        except Exception as e:
            print(f"An error occurred: {e}")
            db.session.rollback()

    return render_template(
        'index.html', 
        no_results=no_results,  # Pass the flag to the template
        tables=[jobs.to_html(classes='data', escape=False)] if jobs is not None and not no_results else [],  # Pass an empty list if tables is None
        titles=titles if jobs is not None and not no_results else None  # Pass the titles only if there are results
    )

@app.route('/clear_session', methods=['POST'])
def clear_session():
    # your code to clear the session
    return 'Session cleared', 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)