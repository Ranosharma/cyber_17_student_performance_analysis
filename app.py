from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Database connection
def get_db():
    conn = sqlite3.connect('student_dashboard.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db()
    students = conn.execute("SELECT * FROM Students").fetchall()
    conn.close()
    return jsonify([dict(row) for row in students])

@app.route("/marks", methods=["GET"])
def get_marks():
    conn = get_db()
    marks = conn.execute("SELECT * FROM Marks").fetchall()
    conn.close()
    return jsonify([dict(row) for row in marks])

@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.get_json()
    conn = get_db()
    conn.execute("INSERT INTO Students (name, email, grade) VALUES (?, ?, ?)",
                 (data['name'], data['email'], data['grade']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student added successfully"})

if __name__ == "__main__":
    app.run(debug=True)
