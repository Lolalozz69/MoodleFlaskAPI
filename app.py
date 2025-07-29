from flask import Flask, jsonify
import moodle_api
import os
from dotenv import load_dotenv

load_dotenv()  # Load token dari .env

app = Flask(__name__)

@app.route('/')
def index():
    return '✅ Moodle Attendance API Live (tanpa DB)'

@app.route('/all')
def get_all():
    data = moodle_api.call("gradereport_user_get_grade_items", courseid=2)["usergrades"]
    cleaned = []

    for u in data:
        gradeitems = u.get("gradeitems", [])
        if len(gradeitems) >= 6:
            cleaned.append({
                "userid": u["userid"],
                "username": u["userfullname"],
                "courseid": u["courseid"],
                "examscore": gradeitems[1]["gradeformatted"],
                "quiztotal": gradeitems[2]["gradeformatted"],
                "journal": gradeitems[3]["gradeformatted"],
                "attendance": gradeitems[4]["gradeformatted"],
                "attendance_plugin": gradeitems[5]["graderaw"]
            })

    return jsonify({"all": cleaned})

@app.route('/attendance')
def get_attendance():
    data = moodle_api.call("gradereport_user_get_grade_items", courseid=2)["usergrades"]
    attendance = []

    for u in data:
        gradeitems = u.get("gradeitems", [])
        if len(gradeitems) >= 6:
            attendance.append({
                "userid": u["userid"],
                "username": u["userfullname"],
                "attendance": gradeitems[5]["gradeformatted"]
            })

    return jsonify({"attendance": attendance})

@app.route('/attendance/<int:userid>')
def get_attendance_by_user(userid):
    data = moodle_api.call("gradereport_user_get_grade_items", courseid=2)["usergrades"]

    for u in data:
        if u["userid"] == userid:
            gradeitems = u.get("gradeitems", [])
            if len(gradeitems) >= 6:
                return jsonify({
                    "userid": u["userid"],
                    "username": u["userfullname"],
                    "attendance": gradeitems[5]["gradeformatted"]
                })

    return jsonify({"error": "User ID not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
