from flask import Flask, request, jsonify, render_template
import os
import pdfplumber
import docx
import pytesseract
import cv2
import numpy as np
from PIL import Image

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

answer_key_data = {}

def preprocess_image(filepath):
    """Enhance image for better OCR accuracy on handwriting"""
    img = cv2.imread(filepath)
    # Resize bigger for better OCR
    img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Remove noise
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    # Adaptive threshold
    thresh = cv2.adaptiveThreshold(
        denoised, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 41, 15
    )
    # Sharpen the image
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(thresh, -1, kernel)
    return sharpened

def extract_text_from_image(filepath):
    """Use Tesseract OCR to read text from image"""
    try:
        processed = preprocess_image(filepath)
        # Try multiple OCR modes and pick best result
        configs = [
            r'--oem 3 --psm 6 -l eng',
            r'--oem 3 --psm 4 -l eng',
            r'--oem 1 --psm 6 -l eng',
        ]
        best_text = ""
        best_count = 0
        for config in configs:
            text = pytesseract.image_to_string(processed, config=config)
            # Count how many q1, q2 etc found
            count = sum(1 for i in range(1, 10) if f'q{i}' in text.lower())
            print(f"Config {config}: found {count} questions")
            print(f"Text: {text}")
            if count > best_count:
                best_count = count
                best_text = text
        print(f"Best OCR text:\n{best_text}")
        return best_text
    except Exception as e:
        print(f"OCR error: {e}")
        return ""

def extract_text(filepath):
    """Extract text from PDF, DOCX, TXT or IMAGE file"""
    text = ""
    ext = filepath.lower().split('.')[-1]

    if ext == 'pdf':
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    elif ext == 'docx':
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"

    elif ext in ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp']:
        text = extract_text_from_image(filepath)

    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

    return text

def fix_ocr_lines(text):
    """Fix common OCR mistakes and merge wrapped lines"""
    # Common OCR character fixes
    fixes = {
        '@1': 'q1', '@2': 'q2', '@3': 'q3', '@4': 'q4',
        '@5': 'q5', '@6': 'q6', '@7': 'q7', '@8': 'q8',
        'ql:': 'q1:', 'q!:': 'q1:', 'gi:': 'q1:',
        'ol:': 'q1:', 'o2:': 'q2:', 'o3:': 'q3:',
        'gl:': 'q1:', 'g2:': 'q2:', 'g3:': 'q3:',
        'al:': 'q1:', 'a2:': 'q2:', 'a3:': 'q3:',
        'qi:': 'q1:', 'qz:': 'q2:',
        '&': 'and', '$': 's',
    }

    lines = text.strip().split('\n')
    fixed_lines = []
    for line in lines:
        line_lower = line.lower().strip()
        for wrong, correct in fixes.items():
            line_lower = line_lower.replace(wrong, correct)
        if line_lower:
            fixed_lines.append(line_lower)

    # Merge wrapped lines
    merged = []
    current = ""
    for line in fixed_lines:
        line = line.strip()
        if not line:
            continue
        # Check if line is a new question
        is_new_q = False
        for i in range(1, 10):
            if line.startswith(f'q{i}:') or line.startswith(f'q{i} :'):
                is_new_q = True
                break
        if is_new_q:
            if current:
                merged.append(current)
            current = line
        else:
            current += " " + line

    if current:
        merged.append(current)

    result = '\n'.join(merged)
    print(f"Fixed and merged text:\n{result}")
    return result

def parse_answer_key(text):
    questions = {}
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        line_lower = line.lower()
        if not (line_lower.startswith('q') and ':' in line_lower):
            continue
        try:
            parts = line.split('|')
            q_part = parts[0].strip()
            q_num = q_part.split(':')[0].strip().lower()

            keywords = []
            marks = 1

            for part in parts[1:]:
                part = part.strip().lower()
                if 'keywords:' in part:
                    kw_text = part.split('keywords:')[1].strip()
                    keywords = [k.strip() for k in kw_text.split(',') if k.strip()]
                elif 'marks:' in part:
                    marks_text = part.split('marks:')[1].strip()
                    marks = int(marks_text)

            questions[q_num] = {
                'keywords': keywords,
                'marks': marks
            }
            print(f"Loaded: {q_num} | keywords: {keywords} | marks: {marks}")
        except Exception as e:
            print(f"Error parsing line: {line} => {e}")
            continue
    return questions

def parse_student_answers(text):
    text = fix_ocr_lines(text)
    answers = {}
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('q') and ':' in line:
            try:
                q_num = line.split(':')[0].strip()
                answer = line.split(':', 1)[1].strip().lower()
                answers[q_num] = answer
                print(f"Student answer: {q_num} => {answer}")
            except Exception as e:
                print(f"Error parsing: {line} => {e}")
                continue
    return answers

def grade_answers(answer_key, student_answers):
    results = []
    total_marks = 0
    marks_obtained = 0

    for q_num, key_data in answer_key.items():
        total_marks += key_data['marks']
        student_ans = student_answers.get(q_num, "")

        keywords_found = []
        keywords_missing = []

        for keyword in key_data['keywords']:
            keyword_clean = keyword.strip().lower()
            if keyword_clean in student_ans.lower():
                keywords_found.append(keyword)
            else:
                keywords_missing.append(keyword)

        if len(key_data['keywords']) > 0:
            keyword_score = len(keywords_found) / len(key_data['keywords'])
            question_marks = round(keyword_score * key_data['marks'], 1)
        else:
            question_marks = key_data['marks'] if student_ans.strip() != "" else 0

        marks_obtained += question_marks
        print(f"{q_num}: found={keywords_found}, missing={keywords_missing}, marks={question_marks}")

        results.append({
            'question': q_num.upper(),
            'marks_allotted': key_data['marks'],
            'marks_obtained': question_marks,
            'keywords_found': keywords_found,
            'keywords_missing': keywords_missing,
            'student_answer': student_ans if student_ans else "No answer found"
        })

    return results, total_marks, marks_obtained

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-answer-key', methods=['POST'])
def upload_answer_key():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'answer_key_' + file.filename)
    file.save(filepath)
    text = extract_text(filepath)
    print("Answer key text:\n", text)
    answer_key_data['key'] = parse_answer_key(text)
    answer_key_data['total_questions'] = len(answer_key_data['key'])
    return jsonify({'message': f"Answer key loaded! Found {answer_key_data['total_questions']} questions."})

@app.route('/grade-student', methods=['POST'])
def grade_student():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    if 'key' not in answer_key_data:
        return jsonify({'error': 'Please upload answer key first!'}), 400

    file = request.files['file']
    student_name = request.form.get('student_name', 'Student')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'student_' + file.filename)
    file.save(filepath)

    text = extract_text(filepath)
    print("Student text:\n", text)
    student_answers = parse_student_answers(text)
    results, total_marks, marks_obtained = grade_answers(answer_key_data['key'], student_answers)

    percentage = round((marks_obtained / total_marks * 100), 1) if total_marks > 0 else 0

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 75:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 45:
        grade = "C"
    elif percentage >= 35:
        grade = "D"
    else:
        grade = "F"

    return jsonify({
        'student_name': student_name,
        'results': results,
        'total_marks': total_marks,
        'marks_obtained': marks_obtained,
        'percentage': percentage,
        'grade': grade
    })

if __name__ == '__main__':
    app.run(debug=True)



