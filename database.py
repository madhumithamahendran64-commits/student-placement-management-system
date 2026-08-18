import sqlite3

connection = sqlite3.connect("placement.db")
cursor = connection.cursor()

# Students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    department TEXT,
    cgpa REAL,
    skills TEXT
)
""")

# Companies table
cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    job_role TEXT NOT NULL,
    location TEXT,
    salary REAL,
    min_cgpa REAL,
    required_skills TEXT
)
""")
# Recreate placements table
cursor.execute("DROP TABLE IF EXISTS placements")

cursor.execute("""
CREATE TABLE placements (
    placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    job_role TEXT,
    location TEXT,
    salary REAL,
    min_cgpa REAL,
    required_skills TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
)
""")


# Applications table
cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    company_id INTEGER,
    application_date TEXT,
    status TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
)
""")

# Sample students
cursor.execute("""
INSERT INTO students
(name, email, password, department, cgpa, skills)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    "Arun",
    "arun@gmail.com",
    "12345",
    "CSE",
    8.5,
    "Python, SQL"
))

cursor.execute("""
INSERT INTO students
(name, email, password, department, cgpa, skills)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    "Priya",
    "priya@gmail.com",
    "12345",
    "CSE",
    9.0,
    "Java, Python"
))

cursor.execute("""
INSERT INTO students
(name, email, password, department, cgpa, skills)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    "Ravi",
    "ravi@gmail.com",
    "12345",
    "ECE",
    7.8,
    "C, Python"
))

connection.commit()
connection.close()

print("Database created successfully!")