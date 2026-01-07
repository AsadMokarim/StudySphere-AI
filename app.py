from flask import Flask, redirect, render_template, request, url_for, session
import os
import json
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


from flask_sqlalchemy import SQLAlchemy

from agents.ocr_agent import ocr_agent
from agents.notes_agent import notes_agent
from agents.quiz_agent import quiz_agent
from agents.doubt_agent import doubt_agent
from agents.llm import ask_gemini



app = Flask(__name__)
app.secret_key = "studysphere-secret-key"



@app.route('/')
def landing_page():
    return redirect(url_for('upload_content'))

    # return render_template('index.html')

@app.route('/upload_content')
def upload_content():
    return render_template('upload.html')



@app.route('/uploaded_content', methods=["POST"])
def uploaded_content():
    files = request.files.getlist('up_file')
    ocr_result = ocr_agent(files) # list data type
    notes_data = notes_agent(ocr_result) #dictionary data type

    action = request.form.get("action")

    # notes_data = {
    #     'EVS-Notes for 1st internal from unit 1_page-0001.jpg': {
    #         'title': 'Environmental Studies: Definition, Scope, and Multidisciplinary Nature',
    #         'summary': 'Environmental Studies is an interdisciplinary field focusing on the relationship between humans and their environment...',
    #         'key_points': [
    #             'Environmental Studies is interdisciplinary',
    #             'Promotes sustainable development'
    #         ],
    #         'formulas': []
    #     }
    # }

    allSummary = []
    for filename, content in notes_data.items():
        allSummary.append({
            "filename": filename,
            "title": content.get("title"),
            "summary": content.get("summary"),
            "key_points": content.get("key_points"),
            "formulas": content.get("formulas")
        })

    session['allSummary'] = allSummary
    if action == 'quiz':
        quiz_options = {
            "quiz_type": request.form.get("quiz_type"),
            "difficulty": request.form.get("difficulty"),
            "num_questions": request.form.get("num_questions")
        }
        session['quiz_options'] = quiz_options
        return redirect(url_for('quiz_route'))

    return redirect(url_for('summary'))





@app.route('/summary')
def summary():
    allSummary = session.get('allSummary', [])
    return render_template('summary.html', allSummary=allSummary)






@app.route('/quiz', methods = ["GET", "POST"])
def quiz_route():
    notes = session.get('allSummary', [])
    quiz_options= session.get('quiz_options', {})
    quiz_data = quiz_agent(notes, quiz_options) #json
    # quiz_data = {
    #     "questions": [
    #         {
    #             "id": "Q1",
    #             "question": "Is Environmental Science a subject?",
    #             "options": ["True", "False"],
    #             "answer": 1
    #         },
    #         {
    #             "id": "Q2",
    #             "question": "Is EVS interdisciplinary?",
    #             "options": ["Yes", "No","Both", "None of the above"],
    #             "answer": 0
    #         },
    #         {
    #             "id": "Q2",
    #             "question": "Is EVS interdisciplinary?",
    #             "options": ["Yes", "No","Both", "None of the above"],
    #             "answer": 0
    #         },
    #         {
    #             "id": "Q2",
    #             "question": "Is EVS interdisciplinary?",
    #             "options": ["Yes", "No","Both", "None of the above"],
    #             "answer": 0
    #         },
    #         {
    #             "id": "Q2",
    #             "question": "Is EVS interdisciplinary?",
    #             "options": ["Yes", "No","Both", "None of the above"],
    #             "answer": 0
    #         },
    #     ]
    # }
    
    return render_template(
        "quiz.html",
        allques=quiz_data["questions"],
        current_index=0,
        answered_count=0
    )




@app.route('/ocr', methods = ["GET", "POST"])
def ocr_route():
    return ocr_agent()
@app.route('/notes', methods = ["GET", "POST"])
def notes_route():
    return notes_agent()



@app.route('/doubt', methods = ["GET", "POST"])
def doubt_route():
    if request.method == "POST":
        prompt = request.form['user_prompt']
        prompt+=" Answer in less than 200 words"
        response = ask_gemini(prompt=prompt)
        return render_template('doubt.html', response= response)
    return render_template('doubt.html', response= None)





@app.route('/results', methods=["POST"])
def results():
    raw = request.form.get("answers")
    data = json.loads(raw)

    correct = 0
    for q in data:
        if q["user_answer"] == q["correct_answer"]:
            q["is_correct"] = True
            correct += 1
        else:
            q["is_correct"] = False

    score = round((correct / len(data)) * 100)
    option_idx = ["A", "B", "C", "D"]
    
    return render_template(
        "results.html",
        questions=data,
        score=score,
        correct=correct,
        total=len(data),
        option_idx = option_idx
    )



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)




