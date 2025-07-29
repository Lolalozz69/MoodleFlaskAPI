from flask import Flask, jsonify
import moodle_api
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    return '✅ Moodle Attendance API (Tanpa DB Lokal) aktif!'


@app.route('/all')
def get_all():
    out = moodle_api.call("gradereport_user_get_grade_items", courseid=2)
    correct_json = out["usergrades"]
    lst_dict = []
    for i in range(len(correct_json)):
        try:
            lst_dict.append({
                'userid': correct_json[i]['userid'],
                'username': correct_json[i]['userfullname'],
                'courseid': correct_json[i]['courseid'],
                'examscore': correct_json[i]['gradeitems'][1]['gradeformatted'],
                'quiztotal': correct_json[i]['gradeitems'][2]['gradeformatted'],
                'journal': correct_json[i]['gradeitems'][3]['gradeformatted'],
                'attendance': correct_json[i]['gradeitems'][4]['gradeformatted'],
                'attendance_plugin': correct_json[i]['gradeitems'][5]['graderaw']
            })
        except IndexError:
            continue

    return jsonify({'all': lst_dict})


@app.route('/attendance')
def get_attendance():
    out = moodle_api.call("gradereport_user_get_grade_items", courseid=2)
    correct_json = out["usergrades"]
    lst_dict = []
    for i in range(len(correct_json)):
        try:
            lst_dict.append({
                'userid': correct_json[i]['userid'],
                'username': correct_json[i]['userfullname'],
                'attendance': correct_json[i]['gradeitems'][5]['gradeformatted']
            })
        except IndexError:
            continue

    return jsonify({'attendance': lst_dict})


@app.route('/attendance/<int:userid>')
def get_attendance_by_user(userid):
    out = moodle_api.call("gradereport_user_get_grade_items", courseid=2)
    correct_json = out["usergrades"]

    for user in correct_json:
        try:
            if user["userid"] == userid:
                return jsonify({
                    "userid": user["userid"],
                    "username": user["userfullname"],
                    "attendance": user["gradeitems"][5]["gradeformatted"]
                })
        except IndexError:
            continue

    return jsonify({"error": "User ID tidak ditemukan"}), 404


if __name__ == '__main__':
    app.run(debug=True)
