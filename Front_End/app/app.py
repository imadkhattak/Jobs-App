from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from Back_End.src.Main import all_jobs
from Back_End.src.llm import explain_matching_jobs
from Back_End.src.cv_parser import extract_text

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)


# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/upload', methods=['POST'])
def upload_cv():
    try:
        # Check if file is present
        if 'cv_file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['cv_file']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF, DOC, or DOCX'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract CV content
        cv_content = extract_text(filepath)
        
        # Get matching jobs
        matching_jobs = explain_matching_jobs(cv_content, all_jobs)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        # Handle case where LLM returns invalid JSON
        if isinstance(matching_jobs, dict) and 'raw_output' in matching_jobs:
            return jsonify({
                'error': 'Unable to process CV. Please try again.',
                'details': 'The AI model returned an unexpected response.'
            }), 500
        
        return jsonify({
            'success': True,
            'jobs': matching_jobs,
            'cv_info': cv_content
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
