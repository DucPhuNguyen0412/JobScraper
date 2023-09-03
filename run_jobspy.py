# Import necessary modules
import sys
sys.path.append('D:\\Job-scraper\\src')

from jobspy import scrape_jobs
import pandas as pd

# Main function
def main():
    # Call the scrape_jobs function and store the DataFrame in 'jobs'
    jobs = scrape_jobs(
        site_name=["indeed", "linkedin", "zip_recruiter"],
        search_term="software engineer",
        results_wanted=10
    )

    # Check if the DataFrame is empty
    if jobs.empty:
        print("No jobs found.")
    else:
        # Configure Pandas display options
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 50)  # set to 0 to see full job url / desc
        
        # Print the DataFrame to the terminal
        print(jobs)

        # Uncomment the line below if you are running this in a Jupyter Notebook
        # display(jobs)

        csv_file = 'jobs.csv'

        # Read existing data from the CSV file
        try:
            old_data = pd.read_csv(csv_file)
        except FileNotFoundError:
            old_data = pd.DataFrame()

        # Concatenate the old data with the new data
        all_data = pd.concat([old_data, jobs], ignore_index=True)

        # Save the DataFrame to a CSV file
        all_data.to_csv(csv_file, index=False)

# Call the main function when the script is executed
if __name__ == "__main__":
    main()
