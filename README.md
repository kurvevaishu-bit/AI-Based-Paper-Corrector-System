
# 📝AI-Based Paper Corrector System

```bash
Author : Vaishu Kurve
Affiliation: Suryoda College of Engineering and Technology
Date: March 2026
```
---

## Abstract
This project presents an AI-Based Paper Corrector System, a web application designed to automate the grading of student answer sheets. Traditional paper evaluation is time-consuming and prone to inconsistency. This system addresses these challenges by enabling teachers to upload an answer key with defined keywords and marks per question, and then upload student answer sheets in various formats including PDF, DOCX, TXT, and handwritten image files. The system extracts text from uploaded files using OCR technology (Tesseract) and compares student responses against the answer key by checking for the presence of predefined keywords. Marks are awarded proportionally based on keyword matches, and a final grade with percentage is calculated automatically. The results are displayed in an intuitive web interface showing question-wise breakdowns, found and missing keywords, and a visual progress bar. Built using Python Flask for the backend and HTML/CSS/JavaScript for the frontend, the system is lightweight, beginner-friendly, and runs locally without requiring cloud infrastructure.

## 1. Introduction

In educational institutions, teachers spend a significant amount of time manually evaluating student answer sheets. This process is not only tedious but can also lead to inconsistent grading due to human fatigue and subjectivity. With the advancement of Artificial Intelligence and Natural Language Processing, there is a growing opportunity to automate and standardize the grading process.
The AI-Based Paper Corrector System aims to solve this problem by providing an automated solution that can read both digital and handwritten answer sheets, extract relevant text, and compare it with a predefined answer key. The system is designed to be simple enough for non-technical users such as school teachers, while still leveraging modern technologies like OCR and keyword-based NLP matching.

### Objectives:
- to develop a web-based grading tool accessible to teachers
- to support multiple file formats including handwritten images
- to provide transparent, question-wise grading feedback
- to reduce evaluation time significantly.
  
---

## 2. Literature Review

Automated grading systems have been an active area of research in educational technology. Early systems like Project Essay Grade (PEG) introduced computational scoring of essays using statistical features. Later, Intelligent Tutoring Systems (ITS) incorporated NLP to provide feedback to students.
Optical Character Recognition (OCR) technology, particularly Tesseract OCR developed by Google, has made it possible to digitize handwritten content. Research has shown that preprocessing techniques such as adaptive thresholding and image sharpening significantly improve OCR accuracy on handwritten text.
Keyword-based evaluation methods have been widely used in short answer grading systems. Studies show that keyword matching, while simpler than semantic similarity approaches, provides reliable results for factual and science-based questions where specific terminology is expected. Tools like Python's NLTK and spaCy have further enabled lightweight NLP processing for educational applications.
Flask, a micro web framework for Python, has been widely adopted for building lightweight educational web applications due to its simplicity and flexibility. Combined with modern frontend technologies, Flask enables rapid development of functional prototypes suitable for academic projects.

---

## 3. Methodology

The system follows a three-stage pipeline. In the first stage, the teacher uploads an answer key file formatted with question numbers, expected keywords, and marks per question. The system parses this file and stores the grading criteria in memory. In the second stage, the teacher uploads a student answer sheet. If the file is an image, Tesseract OCR is applied after preprocessing the image using grayscale conversion, denoising, adaptive thresholding, and sharpening to extract readable text. In the third stage, the extracted student answers are compared with the answer key using keyword matching. Marks are awarded proportionally based on the ratio of keywords found to total keywords per question. The system then calculates the total marks, percentage, and letter grade, which are displayed in a detailed results view.

## 4. Implementation

### Programming Language:

- Python 3.11 — Backend logic, OCR, file processing
- HTML5 / CSS3 / JavaScript — Frontend web interface

### Frameworks / Libraries:
-	Flask — Web framework for backend routing and API
-	Tesseract OCR + pytesseract — Handwriting recognition
-	OpenCV (cv2) — Image preprocessing for better OCR
- Pillow (PIL) — Image handling
-	pdfplumber — PDF text extraction
-	python-docx — Word document text extraction
-	NumPy — Array processing for image operations

### Tools Used:

-	VS Code — Code editor
-	Git & GitHub — Version control and code hosting
-	Tesseract OCR Engine — Installed locally on Windows
-	Browser (Chrome/Edge) — Frontend interface

### Answer Key Format:

The answer key file uses a structured pipe-separated format:
q1: photosynthesis | keywords: chlorophyll, sunlight, glucose | marks: 5

---

### 5. Results and Discussion

The system was tested with multiple student answer sheets in TXT, DOCX, and image formats. For typed digital files (TXT/DOCX), the system achieved 100% text extraction accuracy and correctly identified all keywords, assigning accurate marks in all test cases.
For handwritten image files, OCR accuracy varied based on handwriting clarity and image quality. In tests with clearly written block letters under good lighting, Tesseract successfully extracted approximately 60-70% of keywords. Cursive or joined handwriting presented more challenges, with recognition accuracy dropping significantly.
The grading system correctly calculated proportional marks based on keyword matches. For example, a student answer containing 2 out of 3 expected keywords for a 5-mark question received 3.3 marks, demonstrating accurate partial credit allocation. The percentage and grade calculation (A+, A, B, C, D, F) functioned correctly across all test cases.

### Sample Output:
```bash
Student Sheet   : sample_answer.jpg
Total Questions : 5
Correct         : 3
Partially Correct: 1
Wrong           : 1
Score           : 8.5 / 10 (85%)

Feedback:
Q2 : Missing keyword "photosynthesis"
Q4 : Answer partially correct — missing mention of F=ma formula
Q5 : Incorrect answer
```

---

## 6. How it works:

1.	Handwriting OCR Accuracy: Tesseract OCR struggles with cursive, joined, or unclear handwriting. Recognition accuracy is highly dependent on image quality and writing style.
2.	Keyword-Only Evaluation: The system only checks for exact keyword matches and does not understand synonyms or semantic meaning. A student who uses a correct synonym will not receive marks.
3.	No Persistent Storage: Answer keys and grading data are stored in memory and lost when the server restarts. There is no database integration.
4.	Single Student at a Time: The current system processes one student answer sheet at a time. Bulk grading of multiple students is not supported.
5.	Local Only: The application runs locally and is not deployed to a public server, limiting accessibility for teachers outside the local machine.

  
  ## Answer Key File Format:
  
```bash
Q1: Photosynthesis is the process by which plants use sunlight...
Q2: Newton's second law states F = ma...
Q3: The water cycle has four stages: evaporation, condensation...

```

---
## 7. Limitations

1.	Handwriting OCR Accuracy: Tesseract OCR struggles with cursive, joined, or unclear handwriting. Recognition accuracy is highly dependent on image quality and writing style.
2.	Keyword-Only Evaluation: The system only checks for exact keyword matches and does not understand synonyms or semantic meaning. A student who uses a correct synonym will not receive marks.
3.	No Persistent Storage: Answer keys and grading data are stored in memory and lost when the server restarts. There is no database integration.
4.	Single Student at a Time: The current system processes one student answer sheet at a time. Bulk grading of multiple students is not supported.
5.	Local Only: The application runs locally and is not deployed to a public server, limiting accessibility for teachers outside the local machine.


---

### 8. Future Scope

-	Integrate advanced AI models (such as Google Gemini or Claude API) for semantic understanding, allowing the system to recognize synonyms and paraphrased answers.
-	Add database support (SQLite or MySQL) to store student records, grades, and historical results persistently.
-	Enable bulk grading — allow teachers to upload multiple student answer sheets at once and generate a class-wide results report.
-	Generate downloadable PDF report cards for each student with detailed question-wise feedback.
-	Deploy the application on a cloud platform (such as Heroku or Render) to make it accessible online for teachers and institutions.
-	Add user authentication so each teacher has a secure login and private access to their answer keys and student data.

---

### Conclusion

The AI-Based Paper Corrector System successfully demonstrates the feasibility of using Python, Flask, and OCR technology to automate the grading of student answer sheets. The system supports multiple file formats including handwritten image files and provides transparent, question-wise feedback with proportional marks allocation.
While the current implementation has limitations particularly in handwriting recognition accuracy and semantic understanding, it provides a strong foundation for a more advanced grading system. The project demonstrates key skills in Python web development, REST API design, OCR integration, and frontend development.
This project contributes a practical, open-source tool that can help educators reduce grading time and provide consistent, objective evaluation. With further development incorporating AI-based semantic matching and cloud deployment, this system has the potential to become a valuable tool for educational institutions.

---

### References

6.	Page, E.B., "Project Essay Grade: PEA," in Automated Essay Scoring: A Cross-Disciplinary Perspective, Lawrence Erlbaum Associates, 2003.
7.	Smith, R., "An Overview of the Tesseract OCR Engine," Proceedings of the Ninth International Conference on Document Analysis and Recognition, 2007.
8.	Grinberg, M., Flask Web Development: Developing Web Applications with Python, O'Reilly Media, 2018.
9.	Bradski, G., "The OpenCV Library," Dr. Dobb's Journal of Software Tools, 2000.
10.	GitHub Repository: https://github.com/kurvevaishu-bit/AI-Based-Paper-Corrector-System
11.	Tesseract OCR Documentation: https://tesseract-ocr.github.io/tessdoc/
12.	Flask Documentation: https://flask.palletsprojects.com/
13.	pdfplumber Library: https://github.com/jsvine/pdfplumber

---
