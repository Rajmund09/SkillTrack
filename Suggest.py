import pandas as pd
from collections import Counter
import os


def recommend_skills(user_skills_str, all_job_data):
    """
    MODIFIED: Takes user skills string and a DataFrame,
    RETURNS a dictionary with the score and missing skills.
    """
    print("Analyzing suggestions...")
    
    if not user_skills_str:
        user_skills = set()
    else:
        skills_list = [skill.strip().lower() for skill in user_skills_str.split(',')]
        user_skills = set(skills_list)
        if "" in user_skills:
            user_skills.remove("")
    df = all_job_data.copy()
    df = df.dropna(subset=['skills'])
    df = df[df['skills'].str.lower() != 'n/a']
    if df.empty:
        return {'score': 0, 'missing_skills': [], 'message': 'No job data found.'}

    job_skill_counter = Counter()
    for skills_list in df['skills']:
        skills = [skill.strip().lower() for skill in skills_list.split('|')]
        job_skill_counter.update(skills)
    if not job_skill_counter:
        return {'score': 0, 'missing_skills': [], 'message': 'No skills found in job data.'}

    missing_skills = []
    match_count = 0
    top_10_skills = job_skill_counter.most_common(10)
    top_10_skill_names = {skill[0] for skill in top_10_skills}

    if not top_10_skill_names:
        return {'score': 0, 'missing_skills': [], 'message': 'No top skills found.'}

    for skill in top_10_skill_names:
        if skill in user_skills:
            match_count += 1
        else:
            missing_skills.append((skill, job_skill_counter[skill]))
            
    match_percentage = (match_count / len(top_10_skill_names)) * 100
    
    missing_skills.sort(key=lambda x: x[1], reverse=True)
    
    return {
        'score': round(match_percentage),
        'match_count': match_count,
        'total_top_skills': len(top_10_skill_names),
        'missing_skills': missing_skills
    }