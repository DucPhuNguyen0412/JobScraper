### Credits

This project is based on [JobSpy](https://github.com/cullenwatson/JobSpy). Modifications were made to add new features and optimizations, including a dynamic UI for real-time input and output.

---

# JobScraper

**JobScraper** is a comprehensive job scraping library with a dynamic UI for real-time input and output.

## Features

- Scrapes job postings from **LinkedIn**, **Indeed**, & **ZipRecruiter** simultaneously.
- Aggregates the job postings in a Pandas DataFrame.
- **New**: Dynamic UI to provide inputs and see outputs in real-time.

## Installation

```bash
pip install jobscrape
Python version >= 3.10 required
```

## Feature: Dynamic UI
Execute run_jobspy_ui.py to open the UI. Provide the required parameters in the input fields and click 'Scrape Jobs' to get real-time output in a dynamically generated table.

## Output

## FAQ
Encountering issues with your queries?
Try reducing the number of results_wanted and/or broadening the filters. If problems persist, please submit an issue.

Received a response code 429?
This means you've been blocked by the job board site for sending too many requests. Consider waiting a few seconds, or try using a VPN. Proxy support coming soon.