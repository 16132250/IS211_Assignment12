import sqlite3 as lite

if __name__ == "__main__":
    con = lite.connect('studentquizzes.db')

    with con:
        cur = con.cursor()

        cur.execute("DROP TABLE IF EXISTS students")
        cur.execute(
            """
            CREATE TABLE students(student_id INTEGER PRIMARY KEY, first TEXT, last TEXT)
            """
        )
        cur.execute("DROP TABLE IF EXISTS quizzes")
        cur.execute(
            """
            CREATE TABLE quizzes(quiz_id INTEGER PRIMARY KEY, subject TEXT, questions INT, quiz_date DATE)
            """
        )
        cur.execute("DROP TABLE IF EXISTS students_results")
        cur.execute(
            """
            CREATE TABLE students_results(student_id INT, quiz_id INT, score INT)
            """
        )
