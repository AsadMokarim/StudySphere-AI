from flask import Flask, redirect, render_template, request

from flask_sqlalchemy import SQLAlchemy

from agents.ocr_agent import ocr_agent
from agents.notes_agent import notes_agent
from agents.quiz_agent import quiz_agent
from agents.doubt_agent import doubt_agent



app = Flask(__name__)

@app.route('/')
def landing_page():
    return render_template('index.html')

@app.route('/upload_content')
def upload_content():
    return render_template('upload.html')

@app.route('/ocr', methods = ["GET", "POST"])
def ocr_route():
    return ocr_agent()
@app.route('/notes', methods = ["GET", "POST"])
def notes_route():
    return notes_agent()
@app.route('/quiz', methods = ["GET", "POST"])
def quiz_route():
    return quiz_agent()
@app.route('/doubt', methods = ["GET", "POST"])



def doubt_route():
    return doubt_agent()






if __name__ == "__main__":
    app.run(debug=True)