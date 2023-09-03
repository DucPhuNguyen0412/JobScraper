from pydantic import ValidationError
import pandas as pd
from jobscrape import scrape_jobs

def main():
    try:
        jobs: pd.DataFrame = scrape_jobs(
            site_name=["indeed", "linkedin", "zip_recruiter"],
            search_term="software engineer",
            results_wanted=10
        )
        
        if jobs.empty:
            print("No jobs found.")
        else:
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', 50)
            print(jobs)
            jobs.to_csv('jobs.csv', index=False)

    except ValidationError as e:
        print(f"Validation error occurred: {e}")

if __name__ == "__main__":
    main()
