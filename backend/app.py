import sys
import os

# Ensure the root directory is in the path so we can import 'backend'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from flask import Flask, render_template, request, jsonify
from backend.ml_engine import MLEngine
from backend.file_handler import FileHandler

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'))

# Set max upload to 128MB for large batches
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024

ml_engine = MLEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rank', methods=['POST'])
def rank():
    # Diagnostic Print for Local Terminal
    print("\n--- INCOMING RANKING REQUEST ---")
    
    job_description = request.form.get('job_description', '').strip()
    
    # Capture 'resumes' and 'resumes[]' keys to be bulletproof
    resume_files = request.files.getlist('resumes')
    if not resume_files:
        resume_files = request.files.getlist('resumes[]')
    
    print(f"Total files received: {len(resume_files)}")
    
    if not job_description:
        return jsonify({'error': 'Job description is empty'}), 400
    
    if not resume_files:
        return jsonify({'error': 'No files were detected by the server.'}), 400

    # Extract text from files
    resumes_data = FileHandler.process_uploads(resume_files)
    print(f"Files successfully parsed: {len(resumes_data)}")
    
    if not resumes_data:
        return jsonify({'error': 'Could not extract text from any selected files. Please check formats.'}), 400

    # Process through ML Engine
    try:
        rankings = ml_engine.rank_resumes(job_description, resumes_data)
        print(f"Successfully ranked {len(rankings)} candidates.")
        return jsonify(rankings)
    except Exception as e:
        print(f"ML Processing Failure: {str(e)}")
        return jsonify({'error': f'Ranking engine error: {str(e)}'}), 500

if __name__ == '__main__':
    print(f"Starting server on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
