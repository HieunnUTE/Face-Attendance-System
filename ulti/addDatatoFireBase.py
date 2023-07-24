import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
        "databaseURL": "https://faceattendacerealtime-"
    })
def send_data_to_firebase(line):
    data = {}
    name = None
    date = None
    line_data = line.strip().split(";")
    if date is None:
        date = line_data[0]
        name = line_data[1]
        data[line_data[3].lower()] = line_data[2]
    elif line_data[0] == date and line_data[1] == name:
        data[line_data[3].lower()] = line_data[2]
    else:
        ref = db.reference("attendance").child(date).child(name).update(data)
        date = line_data[0]
        name = line_data[1]
        data = {}
        data[line_data[3].lower()] = line_data[2]
    print(data)
    ref = db.reference("attendance").child(date).child(name).update(data)
