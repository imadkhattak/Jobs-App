import os
import json
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

from .cv_parser import extract_text
from .llm import explain_matching_jobs
from .jobs_cleaner import (
    clean_indeed_data,
    clean_linkedin_data,
    clean_glassdoor_data
)

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Front_End', 'templates'), static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Front_End', 'static'))


# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
SAVED_JOBS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'saved_jobs', 'saved_jobs.json')

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load and clean data once on startup
script_dir = os.path.dirname(os.path.abspath(__file__))
linkedin_path = os.path.join(script_dir, "..", "data", "retrieved_data", "linkedin_jobs.json")
indeed_path = os.path.join(script_dir, "..",  "data", "retrieved_data", "indeed.json")
glassdoor_path = os.path.join(script_dir, "..", "data", "retrieved_data", "glassdoor.json")

with open(linkedin_path, "r", encoding="utf-8") as f:
    linkedin_data = json.load(f)

with open(indeed_path, "r", encoding="utf-8") as f:
    indeed_data = json.load(f)

with open(glassdoor_path, "r", encoding="utf-8") as f:
    glassdoor_data = json.load(f)

cleaned_indeed = clean_indeed_data(indeed_data)
cleaned_linkedin = clean_linkedin_data(linkedin_data)
cleaned_glassdoor = clean_glassdoor_data(glassdoor_data)
all_jobs = cleaned_indeed + cleaned_linkedin + cleaned_glassdoor


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'cv_file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    file = request.files['cv_file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            cv_content = extract_text(filepath)
            matched_jobs = explain_matching_jobs(cv_content, all_jobs)
            return jsonify({'success': True, 'jobs': matched_jobs})
        except Exception as e:
            print(f"Error processing file: {e}")
            return jsonify({'success': False, 'error': 'Unable to process CV. Please try again.'})
        

@app.route('/saved_jobs')
def saved_jobs():
    return render_template('saved_jobs.html')


@app.route('/get_saved_jobs')
def get_saved_jobs():
    if not os.path.exists(SAVED_JOBS_FILE):
        return jsonify({'saved_jobs': []})
    with open(SAVED_JOBS_FILE, 'r', encoding='utf-8') as f:
        saved_jobs = json.load(f)
    return jsonify({'saved_jobs': saved_jobs})


@app.route('/save_job', methods=['POST'])
def save_job():
    job = request.json
    if not os.path.exists(SAVED_JOBS_FILE):
        with open(SAVED_JOBS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    with open(SAVED_JOBS_FILE, 'r+', encoding='utf-8') as f:
        saved_jobs = json.load(f)
        # Avoid duplicates
        if job not in saved_jobs:
            saved_jobs.append(job)
            f.seek(0)
            json.dump(saved_jobs, f, indent=4)
            return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Job already saved'})


if __name__ == '__main__':
    app.run(debug=True)
