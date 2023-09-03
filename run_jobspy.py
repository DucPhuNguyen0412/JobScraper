# Import necessary modules
import sys
sys.path.append('D:\\Job-scraper\\src')
# import secrets
# print(secrets.token_hex(16))

from jobspy import scrape_jobs, JobType  # make sure to import JobType as well
import pandas as pd

# Main function
def main():
    # Get user inputs
    search_term = input("Enter the search term for the job: ")
    location = input("Enter the location (leave empty for any): ")
    distance_str = input("Enter distance from location in miles (leave empty for default): ")
    distance = int(distance_str) if distance_str else None
    
    job_type_str = input("Enter the job type (leave empty for all types): ")
    job_type = JobType[job_type_str.upper().replace(' ', '_')] if job_type_str else None
    
    results_wanted_str = input("Enter the number of results you want (default is 10): ")
    results_wanted = int(results_wanted_str) if results_wanted_str else 10

    # Call the scrape_jobs function and store the DataFrame in 'jobs'
    jobs = scrape_jobs(
        site_name=["indeed", "linkedin", "zip_recruiter"],
        search_term=search_term,
        location=location,
        distance=distance,
        job_type=job_type,
        results_wanted=results_wanted
    )

    # Check if the DataFrame is empty
    if jobs.empty:
        print("No jobs found.")
        return

    # Configure Pandas display options
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)  # set to 0 to see full job url / desc
    
    # Print the DataFrame to the terminal
    print(jobs)

    # Save the DataFrame to a CSV file
    csv_file = 'jobs.csv'
    try:
        old_data = pd.read_csv(csv_file)
    except FileNotFoundError:
        old_data = pd.DataFrame()
    all_data = pd.concat([old_data, jobs], ignore_index=True)
    all_data.to_csv(csv_file, index=False)

# Call the main function when the script is executed
if __name__ == "__main__":
    main()
