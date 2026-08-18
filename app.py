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
@app.route("/companies")
def companies():

    connection = get_db_connection()

    companies = connection.execute(
        "SELECT * FROM companies"
    ).fetchall()

    connection.close()

    return render_template("companies.html", companies=companies)
@app.route("/placements")
def placements():

    connection = get_db_connection()

    placements = connection.execute("""
        SELECT
            placements.placement_id,
            companies.company_name,
            placements.job_role,
            placements.location,
            placements.salary,
            placements.min_cgpa,
            placements.required_skills
        FROM placements
        JOIN companies
        ON placements.company_id = companies.company_id
    """).fetchall()

    connection.close()

    return render_template(
        "placements.html",
        placements=placements
    )
@app.route("/add-placement", methods=["GET", "POST"])
def add_placement():

    if request.method == "POST":

        company_id = request.form["company_id"]
        job_role = request.form["job_role"]
        location = request.form["location"]
        salary = request.form["salary"]
        min_cgpa = request.form["min_cgpa"]
        required_skills = request.form["required_skills"]

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO placements
            (company_id, job_role, location, salary, min_cgpa, required_skills)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            company_id,
            job_role,
            location,
            salary,
            min_cgpa,
            required_skills
        ))

        connection.commit()
        connection.close()

        return "Placement added successfully!"

    return render_template("add_placement.html")
@app.route("/add-company", methods=["GET", "POST"])
def add_company():

    if request.method == "POST":

        company_name = request.form["company_name"]
        job_role = request.form["job_role"]
        location = request.form["location"]
        salary = request.form["salary"]
        min_cgpa = request.form["min_cgpa"]
        required_skills = request.form["required_skills"]

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO companies
            (company_name, job_role, location, salary, min_cgpa, required_skills)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            company_name,
            job_role,
            location,
            salary,
            min_cgpa,
            required_skills
        ))

        connection.commit()
        connection.close()

        return "Company added successfully!"

    return render_template("add_company.html")
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
@app.route("/apply/<int:placement_id>")
def apply(placement_id):

    connection = get_db_connection()

    connection.execute("""
        INSERT INTO applications
        (student_id, company_id, application_date, status)
        SELECT 1, company_id, date('now'), 'Applied'
        FROM placements
        WHERE placement_id = ?
    """, (placement_id,))

    connection.commit()
    connection.close()

    return "Application submitted successfully!"
@app.route("/applications")
def applications():

    connection = get_db_connection()

    applications = connection.execute("""
        SELECT
            applications.application_id,
            students.name,
            companies.company_name,
            applications.application_date,
            applications.status
        FROM applications
        JOIN students
        ON applications.student_id = students.student_id
        JOIN companies
        ON applications.company_id = companies.company_id
    """).fetchall()

    connection.close()

    return render_template(
        "applications.html",
        applications=applications
    )
if __name__ == "__main__":
    app.run(debug=True)