from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)
def get_db_connection():
    connection = sqlite3.connect("placement.db")
    connection.row_factory = sqlite3.Row
    return connection
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/students")
def students():
    connection = get_db_connection()

    students = connection.execute(
        "SELECT * FROM students"
    ).fetchall()

    connection.close()

    return render_template("students.html", students=students)
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        cgpa = request.form["cgpa"]
        skills = request.form["skills"]

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO students
            (name, email, password, department, cgpa, skills)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            email,
            "temporary",
            department,
            cgpa,
            skills
        ))

        connection.commit()
        connection.close()

        return "Student registered successfully!"

    return render_template("register.html")
if __name__ == "__main__":
    app.run(debug=True)