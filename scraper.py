import csv,os,time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from database import create_database, create_table, insert_jobs


def fetch_job_data(role, location="", skill_focus="", experience_level=""):
    role_search = role.replace(" ", "+").replace("/", "%2F") 
    location_search = location.replace(" ", "+")
    url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={role_search}&txtLocation={location_search}"

    print("Setting up browser...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print(f"Fetching data from {url}...")
    driver.get(url)

    jobs = []
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "job-bx"))
        )
        print("Job list found. Parsing jobs...")
        
        job_listings = driver.find_elements(By.CLASS_NAME, "job-bx")

        if not job_listings:
            print("No job listings found on the page.")
            driver.quit()
            return []

        for job in job_listings:
            
            try:
                title = job.find_element(By.TAG_NAME, "h2").text.strip()
            except NoSuchElementException:
                title = "N/A"
            
            try:
                company = job.find_element(By.CLASS_NAME, "joblist-comp-name").text.strip()
            except NoSuchElementException:
                company = "N/A"
            
            try:
                skills_raw = job.find_element(By.CLASS_NAME, "srp-skills").text
                skills_list_final = []
                
                skills_clean = skills_raw.replace(',', '\n')
                skills_list = [s.strip() for s in skills_clean.split('\n') if s.strip()]
                
                for skill_group in skills_list:
                    skills_list_final.extend(skill_group.split(' '))
                
                skills_set = set()
                for skill in skills_list_final:
                    skill_lower = skill.strip().lower()
                    
                    if (skill_lower and 
                        "+more" not in skill_lower and 
                        "more" != skill_lower and
                        not skill_lower.startswith('+') and  
                        len(skill_lower) > 1):
                        
                        skills_set.add(skill_lower)
                
                skills = " | ".join(sorted(list(skills_set)))
                if not skills: skills = "N/A"
                
            except NoSuchElementException:
                skills = "N/A"
            
            job_location = "N/A"
            experience = "N/A"
            try:
                top_details = job.find_elements(By.CSS_SELECTOR, "ul.top-jd-dtl li")
                for item in top_details:
                    item_html = item.get_attribute('innerHTML') 
                    if "srp-icons location" in item_html:
                        job_location = item.text.strip()
                    elif "srp-icons experience" in item_html:
                        experience = item.text.strip()
            except NoSuchElementException:
                pass 

            if skill_focus and skill_focus.lower() not in skills.lower():
                continue
            if experience_level and experience_level.lower() not in experience.lower():
                continue

            jobs.append({
                "title": title,
                "company": company,
                "skills": skills,
                "location": job_location,
                "experience": experience
            })

    except TimeoutException:
        print("Page timed out or no jobs found.")
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
    finally:
        driver.quit()
        print("Browser closed.")

    print(f"Found {len(jobs)} job listings.")
    return jobs


def saveing_csv(jobs, filename="data/job_data.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "location", "experience", "skills"])
        writer.writeheader()
        for job in jobs:
            writer.writerow({
                "title": job['title'],
                "company": job['company'],
                "location": job['location'],
                "experience": job['experience'],
                "skills": job['skills']
            })
    print(f"✅ Job data saved to {filename}.")


if __name__ == "__main__":
    role = input("Enter job role (required): ")
    location = input("Enter location (optional): ")
    experience_level = input("Enter experience level (optional): ")
    skill_focus = input("Enter skill filter (optional): ")
    
    jobs = fetch_job_data(role, location, skill_focus, experience_level)
    
    if jobs:
        saveing_csv(jobs)
        create_database()
        create_table()
        insert_jobs(jobs)
    else:
        print("No jobs found. No data was saved.")