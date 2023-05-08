from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

import sqlite3

USER = "admin"
PASSWORD = "password"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this should be a secret random string'


def get_db_connection():
    """
    Get me a connection to the database
    :return:
    """
    conn = sqlite3.connect('studentquizzes.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def root():
    return render_template("login.html", message=None)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["user"]
        password = request.form["password"]

        if username == USER and password == PASSWORD:
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", message="Wrong User or Password")
    else:
        return render_template("login.html", message=None)


@app.route('/dashboard')
def dashboard():
    quizzes_qry = "select quiz_id, subject, questions, quiz_date from quizzes"

    conn = get_db_connection()
    students = conn.execute("select student_id, first, last from students").fetchall()
    quizzes_dataset = conn.execute(quizzes_qry).fetchall()

    return render_template("dashboard.html", students=students, quizzes=quizzes_dataset)


@app.route('/addstudent', methods=['POST', 'GET'])
def add_student():
    if request.method == 'POST':
        first_name = request.form["first"]
        last_name = request.form["last"]

        conn = get_db_connection()
        conn.execute("INSERT INTO students(FIRST, last) VALUES(?, ?);", (first_name, last_name))
        conn.commit()

        return redirect(url_for("dashboard"))
    else:
        return render_template("add_student.html")


@app.route('/deletestudent/<student_id>')
def delete_student(student_id):
    conn = get_db_connection()
    conn.execute("DELETE from students where student_id = (?);", (student_id,))
    conn.commit()
    return redirect(url_for("dashboard"))


@app.route('/addquiz', methods=['POST', 'GET'])
def add_quiz():
    if request.method == 'POST':
        subject = request.form["subject"]
        questions = request.form["questions"]
        quiz_date = request.form["quiz_date"]

        conn = get_db_connection()
        conn.execute("INSERT INTO quizzes(subject, questions, quiz_date) VALUES(?, ?, ?);", (subject, questions, quiz_date))
        conn.commit()

        return redirect(url_for("dashboard"))



@app.route('/deletequiz/<quiz_id>')
def delete_quiz(quiz_id):
    conn = get_db_connection()
    conn.execute("DELETE from quizzes where quiz_id = (?);", (quiz_id,))
    conn.commit()
    return redirect(url_for("dashboard"))


@app.route('/viewresult/<quiz_id>')
def view_quiz_result(quiz_id):

    conn = get_db_connection()
    quiz = conn.execute("select subject, questions, quiz_date from quizzes WHERE quiz_id = (?);", (quiz_id,)).fetchone()
    quiz_results = conn.execute(
        "SELECT s.first, s.last, score FROM students_results r join students s "
        "on r.student_id = s.student_id where r.quiz_id = (?);", (quiz_id,)
    ).fetchall()

    return render_template("quiz_results.html", quiz=quiz, results=quiz_results)

@app.route('/addquizresult', methods=['POST'])
def add_quiz_result():
    student_id = request.form["student_id"]
    quiz_id = request.form["quiz_id"]
    score = request.form["score"]

    conn = get_db_connection()
    conn.execute("INSERT INTO students_results(student_id, quiz_id, score) VALUES(?, ?, ?);", (student_id, quiz_id, score))
    conn.commit()

    return redirect(url_for("dashboard"))

@app.route('/studentresults/<student_id>')
def student_results(student_id):
    conn = get_db_connection()
    student = conn.execute("SELECT first, last FROM students WHERE student_id = (?);", (student_id,)).fetchone()
    student_results = conn.execute(
        "SELECT q.subject, q.quiz_date, r.score FROM students_results r JOIN quizzes q "
        "ON r.quiz_id = q.quiz_id WHERE r.student_id = (?);", (student_id,)
    ).fetchall()

    return render_template("student_results.html", student=student, results=student_results)



if __name__ == '__main__':
    app.run(debug=True)
