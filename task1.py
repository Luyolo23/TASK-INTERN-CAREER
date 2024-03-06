from bs4 import BeautifulSoup
import requests
import time
import logging

# Set up logging to control the output of the script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_excluded_skills():
    """
    Prompt the user for skills to exclude, separated by commas, and validate the input.
    Ensures the input is not empty or contains only spaces.
    """
    while True:
        excluded_skills = input('Enter skills to exclude, separated by commas (",") ').strip()
        if excluded_skills:
            # Split the input into a list of skills, removing any leading/trailing spaces
            return [skill.strip() for skill in excluded_skills.split(",")]
        else:
            logging.warning("Skills cannot be empty. Please try again.")


def search_for_jobs(excluded_skills):
    """
    This function finds jobs that don't require any of the excluded skills.
    This function fetches job listings from a website, filters them based on the excluded skills,
    and saves the job details to text files.
    """
    try:
        # Attempt to fetch job listings from the website
        job_data_response = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=Python&txtLocation=')
        job_data_response.raise_for_status()  # Raises an HTTPError if the response was unsuccessful
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch jobs: {e}")
        return

    # Parse the HTML content of the page
    job_data_parsed = BeautifulSoup(job_data_response.text, 'lxml')
    # Finds all job listings on the web page
    job_postings = job_data_parsed.find_all('li', class_='clearfix job-bx wht-shd-bx')
    for listing_index, job_posting in enumerate(job_postings):
        # Extracts job details
        posting_date = job_posting.find('span', class_='sim-posted').text
        if 'few' in posting_date:
            company_name = job_posting.find('h3', class_='joblist-comp-name').text.strip()
            job_skills = job_posting.find('span', class_='srp-skills').text.strip()
            more_job_info_link = job_posting.header.h2.a['href']
            # Checks if the job doesn't require any of the excluded skills
            if all(skill not in job_skills for skill in excluded_skills):
                try:
                    # Saves job details to a text file named posts
                    with open(f'posts/{listing_index}.txt', 'w') as job_file:
                        job_file.write(f"Company name: {company_name}\n")
                        job_file.write(f"Skills:{job_skills}\n")
                        job_file.write(f"Job posted:{posting_date}\n")
                        job_file.write(f"More info: {more_job_info_link}\n")
                    logging.info(f'File saved: {listing_index}')
                except IOError as e:
                    logging.error(f"Failed to save file {listing_index}: {e}")


if __name__ == '__main__':
    # Gets the skills to be excluded from the user
    excluded_skills = get_excluded_skills()
    logging.info(f"Filtering out any of these skills: {', '.join(excluded_skills)}")
    while True:
        try:
            # Find the jobs that don't require any of the excluded skills
            search_for_jobs(excluded_skills)
            waiting_time = 2
            logging.info(f'Waiting {waiting_time} minutes...')
            time.sleep(waiting_time * 60)
        except KeyboardInterrupt:
            logging.info("Exiting due to user interrupt.")
            break
