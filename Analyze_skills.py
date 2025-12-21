
import pandas as pd
from collections import Counter
import os

CSV_FILE = "data/job_data.csv"

def analyze_skills():
    """
    Reads the CSV, splits the skills, and counts the most common ones.
    """
    if not os.path.exists(CSV_FILE):
        print(f"Error: File not found at {CSV_FILE}")
        print("Please run Scraper.py first to create the data file.")
        return

    print(f"Analyzing skills from {CSV_FILE}...")
    
    try:
        df = pd.read_csv(CSV_FILE)
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty. No data to analyze.")
        return

    
    df = df.dropna(subset=['skills'])
    df = df[df['skills'].str.lower() != 'n/a']

    if df.empty:
        print("No jobs with valid skills found in the CSV.")
        return

    
    skill_counter = Counter()

   
    for skills_list in df['skills']:
        skills = [skill.strip().lower() for skill in skills_list.split('|')]
        
        skill_counter.update(skills)

    print("\n--- 📊 Top 10 Most In-Demand Skills ---")
    
    if not skill_counter:
        print("No skills found to analyze.")
        return

    for skill, count in skill_counter.most_common(10):
        print(f"{skill.capitalize()}: {count} jobs")

if __name__ == "__main__":
    analyze_skills()