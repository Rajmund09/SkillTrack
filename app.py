import pandas as pd
from flask import Flask, render_template, request, jsonify, send_from_directory

# Import custom modules
from scraper import fetch_job_data, saveing_csv
from database import create_database, create_table, insert_jobs
from Visualize_skills import create_skills_chart, create_locations_chart, create_experience_chart
from Suggest import recommend_skills

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    """Render the main landing/dashboard page."""
    return render_template("index.html")

@app.route("/download-csv")
def download_csv():
    """Download the scraped job data CSV."""
    try:
        return send_from_directory('data', 'job_data.csv', as_attachment=True)
    except FileNotFoundError:
        return "⚠ File not found. Please search job data first.", 404

@app.route("/search", methods=["POST"])
def search():
    """Fetch job data based on user input, analyze, and return results."""
    try:
        data = request.get_json()
        job_role = data.get('role')
        user_skills = data.get('user_skills')

        if not job_role:
            return jsonify({'error': 'Job role is required!'}), 400

        print(f"🔎 Fetching job data for role: {job_role}")
        job_data = fetch_job_data(job_role)

        if not job_data:
            return jsonify({'error': 'No jobs found for this role.'}), 404

        # Save Data
        saveing_csv(job_data)
        create_database()
        create_table()
        insert_jobs(job_data)

        # Convert to DataFrame
        df = pd.DataFrame(job_data)

        # Generate Charts
        skill_chart = create_skills_chart(df)
        loc_chart = create_locations_chart(df)
        exp_chart = create_experience_chart(df)

        # Generate Skill Suggestions
        suggestions = recommend_skills(user_skills, df)

        # Return All Results
        return jsonify({
            'message': f'Found {len(job_data)} job postings.',
            'skill_chart_script': skill_chart[0] if skill_chart else None,
            'skill_chart_div': skill_chart[1] if skill_chart else "<p>No data available.</p>",
            'loc_chart_script': loc_chart[0] if loc_chart else None,
            'loc_chart_div': loc_chart[1] if loc_chart else "<p>No data available.</p>",
            'exp_chart_script': exp_chart[0] if exp_chart else None,
            'exp_chart_div': exp_chart[1] if exp_chart else "<p>No data available.</p>",
            'suggestions': suggestions
        })
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
