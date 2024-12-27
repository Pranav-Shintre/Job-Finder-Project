import os
import spacy
import PyPDF2
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Check if file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Parse PDF file to extract text
def parse_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            page_text = reader.pages[page].extract_text()
            text += page_text
        print("Extracted text:", text)  # Debugging: print extracted text
    return text

# Extract skills from the parsed text using NLP
# Define a list of common skills
predefined_skills = [
    "Python", "Java", "JavaScript", "C++", "React", "Node.js", "SQL", "Docker", "AWS", "Machine Learning", "Deep Learning", "Flask", "Django", "Git", "HTML", "CSS", "Linux"
]

def extract_skills(text):
    # Load pre-trained NLP model from spaCy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Search for predefined skills in the text
    found_skills = [skill for skill in predefined_skills if skill.lower() in text.lower()]
    
    return found_skills

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Create upload folder if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        try:
            file.save(filepath)

            # Parse the PDF and extract text
            text = parse_pdf(filepath)

            # Extract skills from the parsed text
            skills = extract_skills(text)

            # Print extracted skills for debugging
            print("Extracted skills:", skills)

            return jsonify({'message': 'File uploaded and parsed successfully', 'skills': skills}), 200

        except Exception as e:
            return jsonify({'error': f'Error processing the file: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file format. Only PDF and DOCX are allowed.'}), 400

if __name__ == '__main__':
    app.run(debug=True)

