from database import DBQuery as db
from flask import (Flask, jsonify, request)
from flask_jwt_extended import ( JWTManager, create_access_token, create_refresh_token, get_jwt_identity, get_raw_jwt, jwt_required, jwt_refresh_token_required ) 
from flask_bcrypt import Bcrypt
import config
import os

## CLEARING CONSOLE WHENEVER SERVER STARTS/RESTART
if os.name == 'nt':
    os.system('cls')
elif os.name == 'posix':
    os.system('clear')

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "22ca63228513b2fc43ee446c8ed5b4a10ab8b6886da75ddcfec4c660db2cf9d0"
bcrypt = Bcrypt()
jwt = JWTManager(app)

## ADMIN ROUTES --START
@app.route("/admin/login",methods=['POST'])
def authentication():
    user_credentials = request.get_json()
    admin = db.Admin()
    ## FETCHING PASSWORD FROM DATABASE FOR THE REQUESTED ADMIN_ID
    db_res = admin.query('admin_id',user_credentials['user_id'])
    if db_res['status'] == 212:         ## RUNS WHEN THEIR PRESENTS ANY RESULT FOR THE ABOVE QUERY
        ## MATCHING REQ PASSWORD WITH DB PASSWORD
        for db_credentials in db_res['res']:
            if bcrypt.check_password_hash(db_credentials['password'],user_credentials['password']):
                ## JWT TOKEN GENERATION TAKES PLACE
                access_token = create_access_token(identity=user_credentials['user_id'])
                refresh_token = create_refresh_token(identity=user_credentials['user_id'])
                return jsonify({ 
                    'status':'200',
                    'access-token':access_token,
                    'refresh_token':refresh_token,
                    'msg':'login-successful'
                    })
    return jsonify({ 'status':'401','msg':'Invalid UserID/Password' })    


@app.route("/admin/insert",methods=['POST'])
@jwt_required
def insert():
    ## CHECKING VALIDITY OF JWT TOKEN
    user_id = get_jwt_identity()
    admin = db.Admin()
    db_res = admin.query('admin_id',user_id)
    if db_res['status'] == 212:
        req = request.get_json()
        batch = db.Batch(req['programme'],req['branch'],req['section'],req['year_of_pass'])
        res = {}     ## DICTIONARY TO HOLD DATABASE RESPONSE FOR EACH ENROLLMENT INSERTION IN DATABASE
        for enrollment in req['enrollment']:
            res[enrollment] = batch.insert(enrollment)
        return jsonify({ "status" : res })
    else:
        return jsonify({
            'status':'401',
            'msg':'unauthorized user'
        })
## ADMIN ROUTES --END

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
    