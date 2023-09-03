### Credits

This project is based on [JobSpy](https://https://github.com/cullenwatson/JobSpy). Modifications were made to add new features and optimizations, including a dynamic UI for real-time input and output.

---

# JobSpy UI Edition

**JobSpy UI Edition** is a comprehensive job scraping library with a dynamic UI for real-time input and output.

## Features

- Scrapes job postings from **LinkedIn**, **Indeed**, & **ZipRecruiter** simultaneously.
- Aggregates the job postings in a Pandas DataFrame.
- **New**: Dynamic UI to provide inputs and see outputs in real-time.

## Installation

```bash
pip install jobscrape
Python version >= 3.10 required

Usage
Refer to JobSpy_demo.ipynb for a full demonstration or execute run_jobspy_ui.py for the UI version.

python
Copy code
# Example for programmatic usage
from jobscrape import scrape_jobs
import pandas as pd

jobs: pd.DataFrame = scrape_jobs(
    site_name=["indeed", "linkedin", "zip_recruiter"],
    search_term="software engineer",
    results_wanted=10
)
For details on parameters and response schema, refer to the original JobSpy README.

New Feature: Dynamic UI
Execute run_jobspy_ui.py to open the UI. Provide the required parameters in the input fields and click 'Scrape Jobs' to get real-time output in a dynamically generated table.

Output
Refer to the original JobSpy README for sample output.

FAQ
Encountering issues with your queries?
Try reducing the number of results_wanted and/or broadening the filters. If problems persist, please submit an issue.

Received a response code 429?
This means you've been blocked by the job board site for sending too many requests. Consider waiting a few seconds, or try using a VPN. Proxy support coming soon.