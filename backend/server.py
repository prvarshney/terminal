from database import DBQuery as db
from database import config
from flask import Flask
from flask import request
from flask import jsonify
from Crypto.Cipher import AES
from Crypto import Random
import base64
import hashlib

app = Flask(__name__)

def hashify(raw, key):
    BLOCK_SIZE = 16
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
    private_key = hashlib.sha256(key.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    enc = base64.b64encode(iv + cipher.encrypt(raw))
    return enc

def decrypt(enc, key):
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    private_key = hashlib.sha256(key.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))

@app.route("/",methods=['POST'])
def authentication():
    user_credentials = request.get_json()
    admin = db.Admin()
    db_res = admin.query('admin_id',user_credentials['admin_id'])
    for response in db_res['res']:
        if user_credentials['password'] == response['password']:
            res = { "status":"Habibi" }
        else:
            res = { "status":"Not Habibi" }
    return jsonify(res)

@app.route("/admin/insert",methods=['POST'])
def insert():
    req = request.get_json()
    batch = db.Batch(req['programme'],req['branch'],req['section'],req['year_of_pass'])
    for enrollment in req['enrollment']:
        db_res = batch.insert(enrollment)
    res = { "status" : db_res}
    return jsonify(res)

@app.route("/faculty/insert_attendance",methods=['POST'])
def insert_attendance():
    req = request.get_json()
    attendance = db.Attendance(req['faculty_id'],req['subject'],req['programme'],req['branch'],
    req['section'],req['year_of_pass'],req['semester'])
    db_res = attendance.insert(req['attendance_dictionary'])
    res = {"status" : db_res}
    return jsonify(res)

@app.route("/faculty/show_attendance",methods=['POST'])
def show_attendance():
    req = request.get_json()
    attendance = db.Attendance(req['faculty_id'],req['subject'],req['programme'],req['branch'],
    req['section'],req['year_of_pass'],req['semester'])
    db_res = attendance.show_all()
    print(db_res["res"])
    return db_res
   

if __name__ == '__main__':
    app.run(debug=True,port=5001,host="0.0.0.0")
    