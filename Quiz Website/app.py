from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "quiz_app"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

# Home Page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Start Quiz Page
@app.route("/quiz", methods=["GET"])
def start():
    return render_template("quiz.html")

# Display Questions Page
@app.route("/questions", methods=["GET", "POST"])
def questions():
    con = mysql.connection.cursor()

    if request.method == 'POST':
        # Retrieve form data
        question_text = request.form['question_text']
        option_a = request.form['option_a']
        option_b = request.form['option_b']
        option_c = request.form['option_c']
        option_d = request.form['option_d']
        correct_option = request.form['correct_option']

        # Insert question into the database
        sql_insert = "INSERT INTO quiz (question_text, option_a, option_b, option_c, option_d, correct_option) VALUES (%s, %s, %s, %s, %s, %s)"
        con.execute(sql_insert, [question_text, option_a, option_b, option_c, option_d, correct_option])
        mysql.connection.commit()
        flash('Question added successfully!')
        return redirect("/questions")

    # Fetch all questions from the database
    sql_select = "SELECT * FROM quiz"
    con.execute(sql_select)
    questions_data = con.fetchall()
    con.close()
    return render_template("questions.html", questions=questions_data)

# Result Page
@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == 'POST':
        # Calculate score based on submitted answers
        correct_answers = {
            'q1': 'a',  # Replace with your correct answers
            'q2': 'b',
            'q3': 'c',
            'q4': 'd',
            # Add more questions as needed
        }

        wrong_answers = {
            'q1': request.form.get('q1'),
            'q2': request.form.get('q2'),
            'q3': request.form.get('q3'),
            'q4': request.form.get('q4'),
            # Add more answers as needed
        }

        score = sum(1 for key in correct_answers if wrong_answers.get(key) == correct_answers[key])
        correct_answers = score
        wrong_answers = (correct_answers) - score

        con = mysql.connection.cursor()

        # Insert result into the database
        sql_insert = "INSERT INTO quiz_results (score, correct_answers, wrong_answers) VALUES (%s, %s, %s)"
        con.execute(sql_insert, [score, correct_answers, wrong_answers])
        mysql.connection.commit()
        con.close()

        return redirect("/result")

    # Fetch all results from the database
    con = mysql.connection.cursor()
    sql_select = "SELECT * FROM quiz_results"
    con.execute(sql_select)
    results_data = con.fetchall()
    con.close()
    return render_template("result.html", results_data=results_data)

if __name__ == "__main__":
    app.run(debug=True)



