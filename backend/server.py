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
def admin_authentication():
    ## JSON POST MUST CONTAIN KEYS :-
    ## {
    ##     "user_id":<ADMIN LOGIN ID>,
    ##     "password":<ADMIN LOGIN PASSWORD>
    ## }
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
    return jsonify({ 'status':401,'msg':'Invalid UserID/Password' })    

@app.route('/admin/reset',methods=['POST'])
@jwt_required
def admin_update_password():
    ## JSON POST MUST CONTAIN KEYS :-
    ## {
    ##   "current_password":<STRING>,
    ##   "new_password":<STRING>
    ## }
    ## CHECKING VALIDITY OF JWT TOKEN
    user_id = get_jwt_identity()
    admin = db.Admin()
    db_res = admin.query('admin_id',user_id)
    if db_res['status'] == 212:
        ## FETCHING REQUEST OBJECT
        req = request.get_json()
        ## CHECKING OLD CREDENTIALS
        for document in db_res['res']:
            if document['admin_id'] == user_id and bcrypt.check_password_hash(document['password'],req['current_password']):
                db_res = admin.update_password(user_id,req['new_password'])
                return jsonify({
                    'status':db_res,
                    'msg':'password changes successfully'
                })
            else:
                return jsonify({
                    'status':401,
                    'msg':"password doesn't match"
                })
    else:
        return jsonify({
            'status':401,
            'msg':'unauthorized user'
        })

@app.route('/admin/insert',methods=['POST'])
@jwt_required
def admin_batch_insert():
    ## JSON POST MUST CONTAIN KEYS :-
    ## {    
    ##   "programme":<STRING>,
    ##   "branch":<STRING>,
    ##   "section":<STRING>,
    ##   "year_of_pass":<STRING>,
    ##   "enrollment":<LIST OF ENROLLMENT STRINGS THAT NEED TO BE INSERTED IN BATCH COMPRISES OF ABOVE KEYS>
    ## }
    ## CHECKING VALIDITY OF JWT TOKEN
    user_id = get_jwt_identity()
    admin = db.Admin()
    db_res = admin.query('admin_id',user_id)
    if db_res['status'] == 212:
        req = request.get_json()
        batch = db.Batch(req['programme'],req['branch'],req['section'],req['year_of_pass'])
        db_res = {}     ## DICTIONARY TO HOLD DATABASE RESPONSE FOR EACH ENROLLMENT INSERTION IN DATABASE
        for enrollment in req['enrollment']:
            db_res[enrollment] = batch.insert(enrollment)
        ## BINDING DB RESPONSE IN JSON OBJECT
        res = {
            'batch':f"{req['programme']}_{req['branch']}_{req['section']}_{req['year_of_pass']}",
            'status':db_res
        }
        return jsonify(res)
    else:
        return jsonify({
            'status':401,
            'msg':'unauthorized user'
        })

@app.route('/admin/show_all',methods=['POST'])
@jwt_required
def admin_batch_show_all():
    ## JSON POST MUST CONTAIN KEYS :-
    ## {    
    ##   "programme":<STRING>,
    ##   "branch":<STRING>,
    ##   "section":<STRING>,
    ##   "year_of_pass":<STRING>,
    ## }
    ## CHECKING VALIDITY OF JWT TOKEN & AUTHORIZING USER
    user_id = get_jwt_identity()
    admin = db.Admin()
    db_res = admin.query('admin_id',user_id)
    if db_res['status'] == 212:
        ## FETCHING REQUEST OBJECT
        req = request.get_json()
        ## QUERYING BATCH API
        batch = db.Batch(req['programme'],req['branch'],req['section'],req['year_of_pass'])
        db_res = batch.show_all()
        ## BINDING DATABASE RESPONSE INTO JSON OBJECT
        res = {
            'batch':f"{req['programme']}_{req['branch']}_{req['section']}_{req['year_of_pass']}",
            'enrollment':[]
        }
        if db_res['status'] == 302:         ## RUNS WHEN SUCCESSFUL QUERY TAKES PLACE
            res['msg'] = 'query-successful'
            res['status'] = db_res['status']
            for document in db_res['res']:
                res['enrollment'].append(document['enrollment'])
            return jsonify(res)
        else:
            res['status'] = db_res['status']
            res['msg'] = 'query-unsuccessful'
            return jsonify(res)
    else:
        return jsonify({
            'status':401,
            'msg':'unauthorized user'
        })

@app.route('/admin/remove',methods=['POST'])
@jwt_required
def admin_batch_remove():
    ## JSON POST MUST CONTAIN KEYS :-
    ## {    
    ##   "programme":<STRING>,
    ##   "branch":<STRING>,
    ##   "section":<STRING>,
    ##   "year_of_pass":<STRING>,
    ##   "enrollment":<LIST OF ENROLLMENT STRINGS THAT NEED TO BE INSERTED IN BATCH COMPRISES OF ABOVE KEYS>
    ## }
    ## CHECKING VALIDITY OF JWT TOKEN & AUTHORIZING USER
    user_id = get_jwt_identity()
    admin = db.Admin()
    db_res = admin.query('admin_id',user_id)
    if db_res['status'] == 212:
        ## FETCHING REQUEST OBJECT
        req = request.get_json()
        ## QUERYING BATCH API
        batch = db.Batch(req['programme'],req['branch'],req['section'],req['year_of_pass'])
        db_res = {}
        for enrollment in req['enrollment']:
            db_res[enrollment] = batch.remove(enrollment)
        ## BINDING DATABASE RESPONSE INTO JSON OBJECT
        res = {
            'batch':f"{req['programme']}_{req['branch']}_{req['section']}_{req['year_of_pass']}",
            'status':db_res
        }
        return jsonify(res)
    else:
        return jsonify({
            'status':401,
            'msg':'unauthorized user'
        })

@app.route('/admin/remove_all',methods=['POST'])
@jwt_required
def admin_batch_remove_all():
    ## JSON POST MUST CONTAIN KEYS :-
    ## {    
    ##   "programme":<STRING>,
    ##   "branch":<STRING>,
    ##   "section":<STRING>,
    ##   "year_of_pass":<STRING>
    ## }
    ## CHECKING VALIDITY OF JWT TOKEN & AUTHORIZING USER
    user_id = get_jwt_identity()
    admin = db.Admin()
    db_res = admin.query('admin_id',user_id)
    if db_res['status'] == 212:
        ## FETCHING REQUEST OBJECT
        req = request.get_json()
        ## QUERYING BATCH API
        batch = db.Batch(req['programme'],req['branch'],req['section'],req['year_of_pass'])
        db_res = batch.remove_all()
        ## BINDING DATABASE RESPONSE INTO JSON OBJECT
        res = {
            'batch':f"{req['programme']}_{req['branch']}_{req['section']}_{req['year_of_pass']}",
            'status':db_res
        }
        return jsonify(res)
    else:
        return jsonify({
            'status':401,
            'msg':'unauthorized user'
        })

@app.route('/admin/aboutus',methods=['GET'])
def admin_aboutus():
    ## THIS ROUTE DOESN'T REQUIRES ANY JSON OR DATA FROM USER
    return jsonify({
        'developers':'the three musketers group',
        'msg':'for the community by the community',
        'status':'200'
    })
## ADMIN ROUTES --END

## FACULTY ROUTES --START
@app.route("/faculty/login",methods=['POST'])
def faculty_authentication():
    user_credentials = request.get_json()
    faculty = db.Faculty()
    ## FETCHING PASSWORD FROM DATABASE FOR THE REQUESTED FACULTY_ID
    db_res = faculty.query('faculty_id',user_credentials['user_id'])    
    if db_res['status'] == 212:                  ## RUNS WHEN THERE IS SOME RESULT FOR THE ABOVE QUERY
        ## MATCHING REQ PASSWORD WITH DB PASSWORD
        for document in db_res['res']:
            if bcrypt.check_password_hash(document['password'],user_credentials['password']):
                ## JWT TOKEN GENERATION TAKES PLACE
                access_token = create_access_token(identity=user_credentials['user_id'])
                refresh_token = create_refresh_token(identity=user_credentials['user_id'])
                return jsonify({ 
                    'status':'200',
                    'access-token':access_token,
                    'refresh_token':refresh_token,
                    'msg':'login-successful'
                    })
    return jsonify({ 'status':401,'msg':'Invalid UserID/Password' })    

@app.route("/faculty/insert_attendance",methods=['POST'])
def faculty_insert_attendance():
    req = request.get_json()
    attendance = db.Attendance(req['faculty_id'],req['subject'],req['programme'],req['branch'],
    req['section'],req['year_of_pass'],req['semester'])
    db_res = attendance.insert(req['attendance_dictionary'])
    res = {"status" : db_res}
    return jsonify(res)

@app.route("/faculty/show_attendance",methods=['POST'])
def faculty_show_attendance():
    req = request.get_json()
    attendance = db.Attendance(req['faculty_id'],req['subject'],req['programme'],req['branch'],
    req['section'],req['year_of_pass'],req['semester'])
    db_res = attendance.show_all()
    print(db_res["res"])
    return db_res


if __name__ == '__main__':
    app.run(debug=True,port=5001,host="0.0.0.0")
    