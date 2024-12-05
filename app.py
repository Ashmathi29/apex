from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "sports"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/", methods=["GET", "POST"])
def index():
    """Home page to add student records and display them."""
    connection = mysql.connection.cursor()

    if request.method == "POST":
        # Retrieve form data
        student_name = request.form.get("student_name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        reg_number = request.form.get("reg_number")
        year = request.form.get("year")
        sport_name = request.form.get("sport_name")
        date_played = request.form.get("date_played")

        # Insert new record into the database
        insert_query = """
            INSERT INTO students_sports (student_name, age, gender, reg_number, year, sport_name, date_played) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        connection.execute(insert_query, (student_name, age, gender, reg_number, year, sport_name, date_played))
        mysql.connection.commit()
        flash("Student details have been added successfully!", "success")
        return redirect("/")

    # Fetch all records for display
    select_query = "SELECT * FROM students_sports"
    connection.execute(select_query)
    students_sports_records = connection.fetchall()
    connection.close()

    return render_template("index.html", students_sports_records=students_sports_records)

if __name__ == "__main__":
    app.secret_key = "secret123"
    app.run(debug=True)
