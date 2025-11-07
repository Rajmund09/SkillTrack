# 🚀 SkillTrack – Job Skill Analysis & Recommendation System

SkillTrack is a Python-based web application that helps users analyze real-time job market trends for any role (like “Web Developer”, “AI Engineer”, etc.) and extract the **most in-demand skills, top hiring companies, and experience distribution** from job portals.

It also **visualizes the data using interactive charts** and can **store results in MySQL database**.

---

## ✅ Features

✔ Live job data scraping using **Selenium + BeautifulSoup**  
✔ Save results in **CSV and MySQL database**  
✔ Analyze top **skills, experience levels, and hiring companies**  
✔ Interactive Dashboard using **Plotly Dash / Flask + HTML-CSS**  
✔ Smart Skill Recommendations based on job postings  
✔ Future-ready: can be deployed to web (Render / PythonAnywhere)

---

## 📂 Project Structure

SkillTrack/
│
├── app.py # Main Flask app (UI + backend)
├── scraper.py # Selenium-based job scraper
├── Analyze_skills.py # Skill analysis script
├── Visualize_skills.py # Charts using Plotly Dash
├── Suggest.py # AI-based skill suggestion system
├── database.py # MySQL database connection & insert
├── requirements.txt # Dependencies
├── README.md # Documentation
│
├── /templates
│ └── index.html # Frontend UI (Flask)
├── /static
│ └── style.css # Custom CSS styles
└── /data
└── job_data.csv # Saved job dataset (optional)

---

## ⚙️ Installation & Setup

### ✅ 1. Clone the Repository
```bash
git clone https://github.com/Rajmund09/
