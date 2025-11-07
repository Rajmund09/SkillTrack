import pandas as pd
from flask import Flask, render_template, request, jsonify,send_from_directory


from scraper import fetch_job_data, saveing_csv
from database import create_database, create_table, insert_jobs
from Visualize_skills import create_skills_chart, create_locations_chart, create_experience_chart
from Suggest import recommend_skills

app = Flask(__name__)

@app.route("/")
def home():
    """
    Renders the main HTML page (the "face").
    """
    return render_template("index.html")

@app.route("/download-csv")
def download_csv():
    """
    Provides the 'job_data.csv' file for download.
    """
    print("Download request received for CSV...")
    try:
       
        return send_from_directory(
            'data', 'job_data.csv', as_attachment=True
        )
    except FileNotFoundError:
        return "Error: File not found. Please run a search first.", 404

@app.route("/search", methods=["POST"])
def search():
    """
    The "brain function" that runs when the user clicks "Search."
    """
    print("Search request received...")
    try:
        data = request.get_json()
        job_role = data.get('role')
        user_skills = data.get('user_skills')

        if not job_role:
            return jsonify({'error': 'No job role provided.'}), 400

        print(f"Fetching jobs for: {job_role}")
        job_data = fetch_job_data(job_role)
        if not job_data:
            return jsonify({'error': 'No jobs found for this role.'})
        
        print("Saving data to CSV and Database...")
        saveing_csv(job_data)
        create_database()
        create_table()
        insert_jobs(job_data)
        print("Data saved.")
        
        print("Converting to DataFrame for analysis...")
        df = pd.DataFrame(job_data)

        print("Generating charts...")
        skill_chart_comps = create_skills_chart(df)
        loc_chart_comps = create_locations_chart(df)
        exp_chart_comps = create_experience_chart(df)

        print("Generating suggestions...")
        suggestions = recommend_skills(user_skills, df)

        print("Sending all data back to frontend.")
        return jsonify({
            'message': f'Found {len(job_data)} jobs.',
            'skill_chart_script': skill_chart_comps[0] if skill_chart_comps else None,
            'skill_chart_div': skill_chart_comps[1] if skill_chart_comps else "<p>No skill data.</p>",
            'loc_chart_script': loc_chart_comps[0] if loc_chart_comps else None,
            'loc_chart_div': loc_chart_comps[1] if loc_chart_comps else "<p>No location data.</p>",
            'exp_chart_script': exp_chart_comps[0] if exp_chart_comps else None,
            'exp_chart_div': exp_chart_comps[1] if exp_chart_comps else "<p>No experience data.</p>",
            'suggestions': suggestions
        })

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True) 