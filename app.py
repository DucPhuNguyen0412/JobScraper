from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import configparser
import sys
import openai  # Add this if you're going to use GPT-3

# Initialize Config and Flask
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.secret_key = config['DEFAULT']['FLASK_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config['DEFAULT']['DB_URL']

# Read GPT-3 API Key from config.ini
gpt_key = config['DEFAULT']['GPT_KEY']

# Initialize GPT-3 API client
openai.api_key = gpt_key  # Initialize OpenAI API client with the GPT-3 API key

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

def summarize_with_gpt3(text):
    prompt = text + "\n tl;dr:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=60
    )
    summary = response['choices'][0]['text'].strip()
    return summary

@app.route('/', methods=['GET', 'POST'])
def index():
    jobs = None
    titles = None
    no_results = False
    
    if request.method == 'POST':
        try:
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

            if not jobs.empty:
                jobs['job_url'] = jobs['job_url'].apply(lambda x: f'<a href="{x}" target="_blank">Link</a>')

            if jobs.empty:
                no_results = True
                return render_template('index.html', message="No jobs found.")
            
            new_search = JobSearch(
                search_term=search_term,
                location=location,
                distance=distance,
                job_type=job_type,
                results_wanted=results_wanted
            )
            db.session.add(new_search)
            db.session.commit()

            for index, row in jobs.iterrows():
                description = row['description']
                summarized_description = summarize_with_gpt3(description)  # GPT-3 summarization

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
                    description=summarized_description  # Save the summarized description
                )
                db.session.add(new_result)

            db.session.commit()

            titles = jobs.columns.values
            
        except Exception as e:
            print(f"An error occurred: {e}")
            db.session.rollback()

    return render_template(
        'index.html',
        no_results=no_results,
        tables=[jobs.to_html(classes='data', escape=False)] if jobs is not None and not no_results else [],
        titles=titles if jobs is not None and not no_results else None
    )

@app.route('/clear_session', methods=['POST'])
def clear_session():
    return 'Session cleared', 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
