import sys
import os
## APPENDING SYS PATH TO ACCESS LIB MODULES FROM ANYWHERE
sys.path.append( os.path.join( os.getcwd(),'lib') )
sys.path.append( os.path.join( os.getcwd(),'backend','lib') )

from database import DBQuery as db
from flask import (Flask, jsonify, request)
from flask_jwt_extended import ( JWTManager, create_access_token, create_refresh_token, get_jwt_identity, get_raw_jwt, jwt_required, jwt_refresh_token_required )
from flask_bcrypt import Bcrypt
from datetime import datetime,timedelta,timezone
import smtplib
import config
import random
import pymongo 
import json
import templates
import requests
from logger import log

## CLEARING CONSOLE BEFORE STARTING SERVER
if os.name == 'nt':
    os.system('cls')
elif os.name == 'posix':
    os.system('clear')

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "22ca63228513b2fc43ee446c8ed5b4a10ab8b6886da75ddcfec4c660db2cf9d0"
bcrypt = Bcrypt()
jwt = JWTManager(app)

## OTHER METHODS -- START
def send_email_otp(receiver,user_name,otp,function):
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(config.SENDER_EMAIL_ID,config.SENDER_EMAIL_PASSWORD)
        if function == 'EMAIL_VERIFICATION':
            subject = templates.EMAIL_VERIFICATION_SUBJECT
            body = templates.EMAIL_VERIFICATION_BODY
        if function == 'RECOVER_PASSWORD':
            subject = templates.EMAIL_RECOVER_PASSWORD_SUBJECT
            body = templates.EMAIL_RECOVER_PASSWORD_BODY
        msg = f"Subject:{subject}\n\n{body.replace('<user_name>',user_name).replace('<otp>',str(otp))}"
        smtp.sendmail(config.SENDER_EMAIL_ID,receiver,msg)

def send_sms_otp(receiver,user_name,otp,function):
    url = "https://www.fast2sms.com/dev/bulk"
    if function == 'RECOVER_PASSWORD':
        body = templates.SMS_RECOVER_PASSWORD_BODY.replace('<user_name>',user_name).replace('<otp>',str(otp))
    elif function == 'PHONE_VERIFICATION':
        body = templates.SMS_VERIFICATION_BODY.replace('<user_name>',user_name).replace('<otp>',str(otp))
    payload = f"sender_id=FSTSMS&message={body}&language=english&route=p&numbers={receiver}"
    headers = {
        'authorization': config.SENDER_SMS_AUTH,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    log(f'[  INFO  ] SMS API MSG - {response}')

## OTHER METHODS -- END

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

## ROUTE TO GENERATE OTP FOR A PARTICULAR USESR_ID
@app.route('/admin/forgot_password/<user_id>',methods=['GET'])
def admin_forgot_password_generate_otp(user_id):
    ## INPUT IS ACCEPTED THROUGH URLENCODED VARIABLES I.E user_id
    ## CHECKING THE AVAILABILITY OF GIVEN USER_ID IN DATABASE
    admin = db.Admin()
    db_res = admin.query('admin_id',user_id)
    if db_res['status'] == 212:     # RUNS WHEN GIVEN USER_ID EXISTS
        otp_db = db.OTP()
        user_email_ids = []
        user_name = {}
        for res in db_res['res']:
            user_email_ids = res['email_ids']
            user_name = res['admin_name']
        ## GENERATING OTP
        generated_otp = random.randrange(11111111,100000000)
        ## SENDING OTP TO THE USER THROUGH EMAIL
        send_email_otp(
            receiver=user_email_ids,
            user_name=user_name["f_name"],
            otp=generated_otp,
            function='RECOVER_PASSWORD'
        )
        ## INSERTING GENERATED OTP IN OTP_DB FOR AUTHORIZATION
        otp_db.insert(
            user_id=user_id,
            otp=generated_otp,
            function='EMAIL_VERIFICATION'
        )
        ## MASKING EMAIL TO GENERATE REQUIRED RESPONSE
        for index in range(len(user_email_ids)):
            string = user_email_ids[index]
            ## MASKING STRING WITH 'X' AFTER FIRST 4 CHARACTERS AND BEFORE '@' SYMBOL
            string = string[:4] + 'X' * len(string[4:string.find('@')]) + string[string.find('@'):]
            user_email_ids[index] = string
        ## RETURNING RESPONSE
        return jsonify({
            'status':200,
            'msg':'otp sent to the registered email ids',
            'email_ids':user_email_ids
        })
    else:
        return jsonify({
            'status':206,
            'msg':'invalid user id'
        })

## ROUTE TO VERIFY DELIVERED OTP WITH GIVEN OTP
@app.route('/admin/recover_password/',methods=['POST'])
def admin_forgot_password_verify_otp():
    ## JSON POST MUST CONTAIN KEYS :-
    ## {
    ##   "user_id":<STRING>,
    ##   "otp":<INTEGER>
    ##   "new_password":<STRING>
    ## }
    req = request.get_json()
    user_id = req["user_id"]
    otp = req["otp"]
    new_password = req["new_password"]
    ## CHECKING OTP_DB FOR GIVEN USER_ID AND OTP COMBINATIONS
    otp_db = db.OTP()
    db_res = otp_db.query('user_id',user_id)
    if db_res['status'] == 212 :        ## EXECUTES WHEN GIVEN USERID AVAILABLE IN OTP_DB
        ## CHECKING THE VALIDITY OF GIVEN OTP WITH OTP STORED IN DB
        stored_otp = None
        for document in db_res['res']:
            stored_otp = document['otp']
        if otp == stored_otp:       ## EXECUTES WHEN ALL CONDITIONS FULL FILLED TO RESET PASSWORD
            ## CHANGING PASSWORD OF THE GIVEN USER
            admin = db.Admin()
            db_res = admin.update_password(user_id,new_password)
            if db_res == 301:       ## EXECUTES WHEN PASSWORD UPDATED SUCCESSFULLY
                ## REMOVING OTP STORED IN OTP_DB
                otp_db.remove(user_id)
                return jsonify({
                    'status':db_res,
                    'msg':'password changes successfully'
                })
            else:
                return jsonify({
                    'status':db_res,
                    'msg':'failed to reset password, retry'
                })
    return jsonify({
        'status':401,
        'msg':'invalid userid/otp combination'
    })

@app.route('/admin/reset_password',methods=['POST'])
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
@app.route("/faculty/register",methods=["POST"])
def faculty_provisional_registration():
    ## THIS ROUTE INPUTS FACULTY'S DETAILS AND THEN VERIFIES IT WITH MOBILE AND THE EMAIL ADDRESS.
    ## FORM MUST CONTAIN THE FOLLOWING KEYS:-
    ## {
    ##  "faculty_id":<STRING>
    ## "name": <STRING>,
    ## "phone_number": <STRING>,
    ## "email": <STRING>,
    ## "password": <STRING>,
    ## "dob": <STRING IN DD/MM/YY FORMAT>
    ## }
    faculty_id = request.form.get('faculty_id')
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    password = request.form.get('password')
    dob = request.form.get('dob')
    ## PARSING NAME INTO F_NAME,M_NAME AND L_NAME
    ## E.G. SOMYA SINGHAL INTO: { 'f_name':'SOMYA', 'm_name':'', 'l_name':'SINGHAL' }
    name = name.split(' ')
    if len(name) == 1:
        name = {
            'f_name': name[0],
            'm_name': '',
            'l_name': ''
        }
    else:
        name = {
            'f_name': name[0],
            'm_name': ' '.join(name[1:-1]),
            'l_name': name[-1]
        }
    ## PARSING DOB INTO DICTIONARY OBJECT
    ## E.G. 09/11/2001 INTO { 'DAY' : '09', 'MONTH' : '11', 'YEAR':'2001' }
    dob = dob.split('/')
    dob = { 'day':dob[0], 'month':dob[1], 'year':dob[2]}
    ## STORING THESE VALUES IN PROVISIONAL_FACULTY_DATABASE
    provisional_faculty = db.Provisional_Faculty()
    provisional_faculty.insert(
        faculty_id= faculty_id,
        name= name,
        phone_number= phone_number,
        email= email,
        password= password,
        dob= dob
    )
    ## GENERATING OTP FOR EMAIL AND PHONE NUMBER VERIFICATIONS
    email_otp = random.randrange(10000000,100000000)
    phone_otp = random.randrange(10000000,100000000)
    ## STORING OTPS IN DATABASE
    otp_db = db.OTP()
    otp_db.insert(
        hash_id = hash( str(faculty_id) + str(email) + str(phone_number) ),
        otp = phone_otp,
        function = 'PHONE_VERIFICATION'
    )
    otp_db.insert(
        hash_id = hash( str(faculty_id) + str(email) + str(phone_number) ),
        otp = email_otp,
        function = 'EMAIL_VERIFICATION'
    )
    ## SENDING OTP TO THE USER
    send_email_otp(
        receiver = email,
        user_name = name['f_name'],
        otp = email_otp,
        function = 'EMAIL_VERIFICATION'
    )
    ## SENDING SMS OTP TO THE USER
    send_sms_otp(
        receiver = phone_number,
        user_name = name['f_name'],
        otp = phone_otp,
        function = 'PHONE_VERIFICATION'
    )

    return jsonify({
        'status': 200,
        'msg': 'provisional account created successfully, please verify your email and phone number.'
    })

@app.route('/faculty/verify_email',methods=['POST'])
def faculty_verify_email():
    ## THIS ROUTE INPUTS JSON VALUES THROUGH POST REQUEST 
    ## {
    ##   "faculty_id": <STRING>,
    ##   "email_id": <STRING>,
    ##   "phone_number": <STRING>,
    ##   "email_otp": <INTEGER>
    ## }
    req = request.get_json()
    ## FETCHING EMAIL_OTP STORED IN THE DATABASE FOR VERIFICATION
    otp_db = db.OTP()
    hash_id = hash( req['faculty_id'] + req['email_id'] + req['phone_number'])
    db_res = otp_db.query('hash_id',hash_id)
    if db_res['status'] == 212:
        for document in db_res['res']:
            if document['function'] == 'EMAIL_VERIFICATION':
                if int(document['otp']) == req['email_otp'] :
                    ## UPDATING PROVISIONAL_FACULTY_DB AND VALIDATING EMAIL ADDRESS PROVIDED BY USER
                    provisional_faculty = db.Provisional_Faculty()
                    provisional_faculty.update(hash_id,'email_verification_status',True)
                    ## REMOVING EMAIL VERIFICATION OTP FROM OTP_DB
                    otp_db.remove(hash_id,'EMAIL_VERIFICATION')
                    ## CHECKING WHETHER EMAIL AND PHONE NUMBER BOTH GOT VERIFIED
                    db_res = provisional_faculty.query('hash_id',hash_id)
                    if db_res['status'] == 212:
                        for document in db_res['res']:
                            if document['phone_number_verification_status'] and document['email_verification_status']:
                                ## THIS BLOCK EXECUTES WHEN BOTH EMAIL AND PHONE NUMBERS GOT VERIFIED
                                faculty = db.Faculty()
                                faculty.insert(
                                    id=document['faculty_id'],
                                    name=document['name'],
                                    dob=document['dob'],
                                    phone_number=document['phone_number'],
                                    email=document['email'],
                                    password=document['password'],
                                )
                                ## HENCE FACULTY DOCUMENT TRANSFERS FROM PROVISIONAL_DB TO FACULTY_DB
                                ## NOW REMOVING FACULTY DOCUMENT FROM PROVISIONAL DB
                                provisional_faculty.remove('hash_id',hash_id)
                    return jsonify({
                        'status':200,
                        'msg': 'email address validated successfully'
                    })
                else:
                    return jsonify({
                        'status':401,
                        'msg':'otp mismatch'
                    })
    return jsonify({
        'status':404,
        'msg':'otp not found in database, please try to regenerate otp'
    })

@app.route('/faculty/verify_phone',methods=['POST'])
def faculty_verify_phone():
    ## THIS ROUTE INPUTS JSON VALUES THROUGH POST REQUEST 
    ## {
    ##   "faculty_id": <STRING>,
    ##   "email_id": <STRING>,
    ##   "phone_number": <STRING>,
    ##   "sms_otp": <INTEGER>
    ## }
    req = request.get_json()
    ## FETCHING EMAIL_OTP STORED IN THE DATABASE FOR VERIFICATION
    otp_db = db.OTP()
    hash_id = hash( req['faculty_id'] + req['email_id'] + req['phone_number'])
    db_res = otp_db.query('hash_id',hash_id)
    if db_res['status'] == 212:
        for document in db_res['res']:
            if document['function'] == 'PHONE_VERIFICATION':
                if int(document['otp']) == req['sms_otp'] :
                    ## UPDATING PROVISIONAL_FACULTY_DB AND VALIDATING EMAIL ADDRESS PROVIDED BY USER
                    provisional_faculty = db.Provisional_Faculty()
                    provisional_faculty.update(hash_id,'phone_number_verification_status',True)
                    ## REMOVING EMAIL VERIFICATION OTP FROM OTP_DB
                    otp_db.remove(hash_id,'PHONE_VERIFICATION')
                    ## CHECKING WHETHER EMAIL AND PHONE NUMBER BOTH GOT VERIFIED
                    db_res = provisional_faculty.query('hash_id',hash_id)
                    if db_res['status'] == 212:
                        for document in db_res['res']:
                            if document['phone_number_verification_status'] and document['email_verification_status']:
                                ## THIS BLOCK EXECUTES WHEN BOTH EMAIL AND PHONE NUMBERS GOT VERIFIED
                                faculty = db.Faculty()
                                faculty.insert(
                                    id=document['faculty_id'],
                                    name=document['name'],
                                    dob=document['dob'],
                                    phone_number=document['phone_number'],
                                    email=document['email'],
                                    password=document['password'],
                                )
                                ## HENCE FACULTY DOCUMENT TRANSFERS FROM PROVISIONAL_DB TO FACULTY_DB
                                ## NOW REMOVING FACULTY DOCUMENT FROM PROVISIONAL DB
                                provisional_faculty.remove('hash_id',hash_id)
                    return jsonify({
                        'status':200,
                        'msg': 'phone number validated successfully'
                    })
                else:
                    return jsonify({
                        'status':401,
                        'msg':'otp mismatch'
                    })
    return jsonify({
        'status':404,
        'msg':'otp not found in database, please try to regenerate otp'
    })

@app.route("/faculty/check_availability",methods=['POST'])
def faculty_check_userid_availability():
    ## JSON POST MUST CONTAIN KEYS :-
    ## {
    ##     "user_id":<FACULTY_ID>,
    ## }
    req = request.get_json()
    user_id = req['user_id']
    ## ESTABLISHING CONNECTION WITH FACULTY_DB
    faculty = db.Faculty()
    db_res = faculty.query('faculty_id',user_id)
    if db_res['status'] == 212: # EXECUTES WHEN SUCH FACULTY_ID AVAILABLE IN FACULTY_DB
        return jsonify({
            'status':206,
            'msg':'given user_id is unavailable to use'
        })
    else:
        return jsonify({
            'status':200,
            'msg':'given user_id is available to use'
        })

@app.route("/faculty/login",methods=['POST'])
def faculty_authentication():
    ## JSON POST MUST CONTAIN KEYS :-
    ## {
    ##     "user_id":<FACULTY_ID>,
    ##     "password":<FACULTY LOGIN PASSWORD>
    ## }
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

@app.route("/faculty/view_profile",methods=['POST'])
@jwt_required
def faculty_view_profile():
    ## THIS API IS USED TO VIEW ALL THE DETAILS OF THE FACULTY STORED IN FACULTY_DB.
    ## IT DOESN'T TAKE ANY INPUT.
    faculty_id = get_jwt_identity()
    faculty = db.Faculty()
    db_res = faculty.query('faculty_id',faculty_id)
    new_document = {}
    if db_res['status']==212:
        for document in db_res['res']:
            for key in document:
                if key!='password' and key!='_id':
                    new_document[key]= document[key]
        return jsonify(new_document)
    else:
        return jsonify({
            'msg': 'Unsuccessful Query for faculty_id or faculty_id is wrong.',
            'status': 206
        })

@app.route("/faculty/reset_password",methods=['POST'])
@jwt_required
def faculty_update_password():
    ## JSON POST MUST CONTAIN KEYS :-
    ## {
    ##     "current_password":<STRING>,
    ##     "new_password":<STRING>
    ## }
    user_id = get_jwt_identity()
    ## FETCHING REQUEST OBJECT
    req = request.get_json()
    ## FETCHING PASSWORD STORED OF GIVEN USER_ID IN DATABASE
    faculty = db.Faculty()
    db_res = faculty.query('faculty_id',user_id)
    if db_res['status'] == 212:     ## EXECUTES WHEN GIVEN USER_ID AVAILABLE IN DATABASE
        for document in db_res['res']:
            if document['faculty_id'] == user_id and bcrypt.check_password_hash(document['password'],req['current_password']):
                db_res = faculty.update( user_id,'password',bcrypt.generate_password_hash(req['new_password']).decode('utf-8') )
                if db_res == 301:
                    return jsonify({
                        'status':db_res,
                        'msg':'password changes successfully'
                    })
                else:
                    return jsonify({
                        'status':db_res,
                        'msg':'error encountered while changing password. Retry again.'
                    })
            return jsonify({
                'status':401,
                'msg':"password doesn't match"
            })
    else:
        return jsonify({
            'status':401,
            'msg':"unauthorized user"
        })

@app.route("/faculty/update_profile",methods=['POST'])
@jwt_required
def faculty_update_profile():
    ## THIS ROUTE IS USE TO UPDATE THE FOLLOWING VALUES IN DOCUMENT :
    ## 1. SUBJECTS
    ## 2. QUALIFICATIONS
    ## 3. TIME-TABLE
    ## 4. CLASSES
    ##
    ## JSON POST MUST CONTAIN KEYS :-
    ## {
    ##     <UPDATION_PARAMETER_1>:<UPDATION_VALUE>,
    ##     <UPDATION_PARAMETER_2>:<UPDATION_VALUE>,
    ##     <UPDATION_PARAMETER_3>:<UPDATION_VALUE>,
    ##       ...                       ...
    ##     <UPDATION_PARAMETER_N>:<UPDATION_VALUE>,
    ## }
    ## FOR EXAMPLE :-
    ## {
    ## 	"subjects":subjects,
    ##  "qualifications":qualifications,
    ##  "time-table":time_table,
    ##  "classes":classes
    ## }
    ##
    user_id = get_jwt_identity()
    req = request.get_json()
    ## CONNECTING WITH FACULTY_DB
    faculty = db.Faculty()
    flag = False        # FLAG THAT STATES WHETHER UPDATION QUERY WENT SUCCESSFUL OR NOT
    for key in req:
        db_res = faculty.update(user_id,key,req[key])
        if db_res != 301:
            flag = True
    if flag:
        return jsonify({
            "status":204,
            "msg":"some parameters failed to update, please try again."
        })
    else:
        return jsonify({
            "status":301,
            "msg":"updation successful"
        })

@app.route("/faculty/forgot_password/<user_id>",methods=['GET'])
def faculty_forgot_password_generate_otp(user_id):
    ## ROUTE TO GENERATE FORGOT PASSWORD OTP FOR A PARTICULAR USESR_ID
    ## INPUT IS ACCEPTED THROUGH URLENCODED VARIABLES I.E user_id
    ## ESTABILISHING CONNECTION WITH FACULTY_DB
    faculty = db.Faculty()
    db_res = faculty.query('faculty_id',user_id)
    if db_res['status'] == 212:     # EXECUTES WHEN GIVEN USER_ID AVAILABLE IN THE DATABASE
        otp_db = db.OTP()
        ## GENERATING OTP
        generated_otp = random.randrange(11111111,100000000)
        for document in db_res['res']:
            user_email_id = document['email']
            user_phone_number = document['phone_number']
            user_name = document['name']['f_name']
            ## SENDING OTP TO THE USER THROUGH EMAIL
            send_email_otp(
                receiver=user_email_id,
                user_name=user_name,
                otp=generated_otp,
                function='RECOVER_PASSWORD'
            )
            ## SENDING OTP THROUGH MOBILE NUMBER
            send_sms_otp(
                receiver=user_phone_number,
                user_name=user_name,
                otp=generated_otp,
                function='RECOVER_PASSWORD'
            )
            ## INSERTING GENERATED OTP IN OTP_DB FOR AUTHORIZATION
            otp_db.insert(
                hash_id=hash( user_id+'FORGOT_PASSWORD_HASH' ),
                otp=generated_otp,
                function='RECOVER_PASSWORD'
            )
            ## MASKING EMAIL TO GENERATE REQUIRED RESPONSE
            ## MASKING STRING WITH 'X' AFTER FIRST 4 CHARACTERS AND BEFORE '@' SYMBOL
            user_email_id = user_email_id[:4] + 'X' * len(user_email_id[4:user_email_id.find('@')]) + user_email_id[user_email_id.find('@'):]
            user_phone_number = str(user_phone_number)  # CONVERTING FROM INT64 TO STRING 
            user_phone_number = user_phone_number[:4] + 'X' * len(user_phone_number[4:])
            ## RETURNING RESPONSE
            return jsonify({
                'status':200,
                'msg':'otp sent to the registered email id and phone number',
                'email_id':user_email_id,
                'phone_number':user_phone_number
            })
    else:
        return jsonify({
            "status":206,
            "msg" :"invalid user id"
        })

@app.route("/faculty/recover_password",methods=['POST'])
def faculty_forgot_password_verify_otp():
    ## ROUTE TO VERIFY RECOVER PASSWORD OTP DELIEVERED WITH GIVEN OTP
    ## JSON POST MUST CONTAIN KEYS :-
    ## {
    ##   "user_id":<STRING>,
    ##   "otp":<INTEGER>
    ##   "new_password":<STRING>
    ## }
    req = request.get_json()
    ## ESTABLISHING CONNECTION WITH OTP_DB
    otp_db = db.OTP()
    db_res = otp_db.query('hash_id',hash( req['user_id']+'FORGOT_PASSWORD_HASH' ))
    if db_res['status'] == 212 :    # EXECUTES WHEN GIVEN USER_ID HASH AVAILABLE IN OTP_DB
        stored_otp = None
        for document in db_res['res']:
            stored_otp = document['otp']
        if req['otp'] == stored_otp:       ## EXECUTES WHEN ALL CONDITIONS FULL FILLED TO RESET PASSWORD
            ## CHANGING PASSWORD OF THE GIVEN USER
            faculty = db.Faculty()
            db_res = faculty.update( req['user_id'],'password',bcrypt.generate_password_hash(req['new_password']).decode('utf-8') )
            if db_res == 301:
                ## REMOVING OTP STORED IN OTP_DB
                otp_db.remove( hash( req['user_id']+'FORGOT_PASSWORD_HASH' ),function='RECOVER_PASSWORD' )
                return jsonify({
                    'status':db_res,
                    'msg':'password changes successfully'
                })
            else:   ## EXECUTES WHEN UPDATION FAILED AT DATABASE ENDS DUE TO NETWORK PROBLEM
                return jsonify({
                    'status':db_res,
                    'msg':'failed to reset password, retry'
                })
    ## EXECUTES WHEN EITHER OTP DOESN'T AVAILABLE IN OTP_DB OR OTP GIVEN IS INVALID
    return jsonify({
        'status':401,
        'msg':'invalid userid/otp combination'
    })

@app.route("/faculty/schedule/<faculty_id>",methods=['GET'])
def faculty_show_schedule(faculty_id):
    ## THIS ROUTE IS USE TO FETCH TIMETABLE OF A PARTICULAR FACULTY
    ## ANYONE WITH VALID FACULTY_ID CAN VIEW THE TIME-TABLE OF A PARTICULAR FACULTY
    faculty = db.Faculty()
    db_res = faculty.query('faculty_id',faculty_id)
    if db_res['status'] == 212: # EXECUTES WHEN FACULTY WITH GIVEN FACULTY_ID AVAILABLE IN FACULTY_DB
        for document in db_res['res']:
            time_table = document['time-table'] 
            return jsonify({
                'status':200,
                'time-table':time_table
            })
    else:   # EXECUTES WHEN FACULTY WITH GIVEN FACULTY_ID IS UNAVAILABLE
        return jsonify({
            'status':db_res['status'],
            'msg':'faculty with given faculty id is not available in database'
        })

@app.route("/faculty/insert_current_batch",methods=['POST'])
@jwt_required
def faculty_insert_current_batch():
    ## THIS ROUTE IS USED TO INSERT BATCH THAT A FACULTY CURRENTLY HAVE
    ## JSON POST MUST CONTAIN KEYS :-
    ## {
    ##   "programme":<STRING>,
    ##   "branch":<STRING>,
    ##   "section":<STRING>,
    ##   "semester":<STRING>,
    ##   "subject":<STRING>,
    ##   "year_of_pass":<STRING>
    ## }
    ##
    req = request.get_json()
    faculty_id = get_jwt_identity()
    current_batches = db.CurrentBatches(faculty_id=faculty_id)
    db_res = current_batches.insert(
        subject=req['subject'],
        semester=req['semester'],
        programme=req['programme'],
        branch=req['branch'],
        section=req['section'],
        year_of_pass=req['year_of_pass']
    )
    if db_res == 201:
        return jsonify({
            'status':201,
            'msg':'insertion successfull in database'
        })
    else:
        return jsonify({
            'status':417,
            'msg':'insertion failed'
        })

@app.route("/faculty/fetch_current_batch",methods=['GET'])
@jwt_required
def fetch_current_batch():
    ## THIS API IS USED FOR FETCHING THE DETAILS OF ALL THE CURRENT_BATCHES FOR THE FACULTY.
    ## IT GIVES A LIST OF ALL THE CURRENT_BATCHES OF THE PARTICULAR FACULTY.
    ## CHECKING VALIDITY OF JWT TOKEN
    faculty_id = get_jwt_identity()
    current_batches = db.CurrentBatches(faculty_id)
    db_res = current_batches.show_all()
    current_batches = []
    if db_res['status'] == 302:
        for document in db_res['res']:
            current_batches.append(document['batch'])
        return jsonify({
            'current_batches':current_batches,
            'msg':'Current_batches displayed successfully.',
            'status':201
        })
    else:
        return jsonify({
            'status':401,
            'msg':'unauthorized user'
        })

@app.route("/faculty/fetch_students_list/<batch_name>",methods=['GET'])
@jwt_required
def fetch_students_list(batch_name):
    ## THIS API IS USED TO FETCH THE STUDENT'S LIST OF THE CURRENT BATCH.
    ## IT DISPLAYS ALL THE STUDENT IN A PARTICULAR CLASS.
    ## THERE IS NO JSON OBJECT IN THE BODY.
    ## CHECKING VALIDITY OF JWT TOKEN & AUTHORIZING USER
    faculty_id = get_jwt_identity() 
    batch_name = batch_name.split('_')
    generic_batch_name = ['programme','branch','section','year_of_pass']
    batch_name_dict = {}
    for i in range(len(batch_name)):
        batch_name_dict[generic_batch_name[i]]=batch_name[i]             
    batch = db.Batch(batch_name_dict['programme'],batch_name_dict['branch'],
    batch_name_dict['section'],batch_name_dict['year_of_pass'])
    faculty = db.Faculty()
    student = db.Student()
    db_res = faculty.query('faculty_id',faculty_id)
    if db_res['status'] == 212:              # RUNS WHEN GIVEN FACULTY_ID EXISTS
        otp_db = db.OTP()
        ## GENERATING OTP
        generated_otp = random.randrange(11111111,100000000)
        otp_db.insert(faculty_id,generated_otp)
        batch_res = batch.show_all()
        students_list = []
        for enr in batch_res['res']:
            student_res = student.query("enrollment",enr["enrollment"])
            for j in student_res["res"]:
                students_list.append({
                    "enrollment": j["enrollment"],
                    "rollno": j["rollno"],
                    "name": j["name"]
                })
        return jsonify({
            'otp': generated_otp,
            'students_in_class' : students_list,
            'status' : 200,
            'msg' : 'Student"s list of a particular class is displayed.'
        })
    else:
        return jsonify({
            'status':206,
            'msg':'invalid user id'
        })
## FACULTY ROUTES --END

## STUDENT ROUTES --START
@app.route("/student/register",methods=["POST"])
def student_provisional_registration():
    ## THIS ROUTE INPUTS USER_DETAILS AND BINARY IMAGE OF ID CARD AND STORE THAT IN PROVISIONAL STUDENT RECORD DATABASE
    ## AT THE SAME TIME IT SENDS OTP TO CONTACT EMAIL ADDRESS AND PHONE NUMBERS
    ## FORM MUST CONTAINS THE FOLLOWING KEYS :-
    ## {
    ##   "enrollment": <STRING>,
    ##   "rollno": <STRING>,
    ##   "name": <STRING>,
    ##   "phone_number": <STRING>,
    ##   "email": <STRING>,
    ##   "password": <STRING>.
    ##   "father_name": <STRING>
    ##   "year_of_join": <STRING>,
    ##   "year_of_pass": <STRING>,
    ##   "programme": <STRING>,
    ##   "branch": <STRING>,
    ##   "section": <STRING>,
    ##   "gender": <STRING>,
    ##   "dob": <STRING IN DD/MM/YYYY FORMAT>,
    ##   "temp_addr": <STRING>,
    ##   "perm_addr": <STRING>,
    ##   "identity_proof": <JPEG OR JPG IMAGE>
    ## }
    enrollment = request.form.get('enrollment')
    rollno = request.form.get('rollno')
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    password = request.form.get('password')
    father_name = request.form.get('father_name')
    year_of_join = request.form.get('year_of_join')
    year_of_pass = request.form.get('year_of_pass')
    programme = request.form.get('programme')
    branch = request.form.get('branch')
    section = request.form.get('section')
    gender = request.form.get('gender')
    dob = request.form.get('dob')
    temp_addr = request.form.get('temp_addr')
    perm_addr = request.form.get('perm_addr')
    identity_proof = request.files['image']

    ## PARSING NAME INTO F_NAME, M_NAME AND L_NAME
    ## EG: PRASHANT VARSHNEY INTO { 'f_name':'PRASHANT','m_name':'','l_name':'VARSHNEY' }
    name = name.split(' ')
    if len(name) == 1:
        name = {
            'f_name':name[0],
            'm_name':'',
            'l_name':''
        }
    else:
        name = {
            'f_name':name[0],
            'm_name':' '.join(name[1:-1]),
            'l_name':name[-1]
        }
    ## PARSING FATHER_NAME INTO F_NAME, M_NAME AND L_NAME
    ## EG: PRASHANT VARSHNEY INTO { 'f_name':'PRASHANT','m_name':'','l_name':'VARSHNEY' }
    father_name = father_name.split(' ')
    if len(father_name) == 1:
        father_name = {
            'f_name':father_name[0],
            'm_name':'',
            'l_name':''
        }
    else:
        father_name = {
            'f_name':father_name[0],
            'm_name':' '.join(father_name[1:-1]),
            'l_name':father_name[-1]
        }
    ## MODIFYING IDENTITY_PROOF FILENAME SO THAT NO TWO FILES WILL HAVE SAME NAME
    identity_proof_filename = str(hash(''.join(identity_proof.filename.split('.')[:-1]) + datetime.now().strftime('%H%M%S'))) + '.' + identity_proof.filename.split('.')[-1] 
    ## PARSING DOB INTO DICTIONARY OBJECT
    ## EG: 04/06/1998 INTO { 'DAY':'04','MONTH':'06','YEAR':'1998' }
    dob = dob.split('/')
    dob = { 'day':dob[0],'month':dob[1],'year':dob[2] }
    ## STORING THESE VALUES IN PROVISONAL_STUDENT_DATABASE
    provisional_student = db.Provisional_Student()
    provisional_student.insert(
        enrollment=enrollment,
        rollno=rollno,
        name=name,
        phone_number=phone_number,
        email=email,
        password=password,
        father_name=father_name,
        year_of_join=year_of_join,
        year_of_pass=year_of_pass,
        programme=programme,
        branch=branch,
        section=section,
        gender=gender,
        dob=dob,
        temp_address=temp_addr,
        perm_address=perm_addr,
        identity_proof=identity_proof_filename
    )
    ## SAVING IDENTITY PROOF IN DATABASE FOR MANUAL VERIFICATION
    identity_proof.save( os.path.join(os.getcwd(), 'uploads' , identity_proof_filename ))
    ## GENERATING OTP FOR EMAIL AND PHONE NUMBER VERIFICATIONS
    email_otp = random.randrange(10000000,100000000)
    phone_otp = random.randrange(10000000,100000000)
    ## STORING OTPS IN DATABASE
    otp_db = db.OTP()
    otp_db.insert(
        hash_id=hash( str(enrollment) + str(email) + str(phone_number) ),
        otp=email_otp,
        function='EMAIL_VERIFICATION'
    )
    otp_db.insert(
        hash_id=hash( str(enrollment) + str(email) +str(phone_number)  ),
        otp=phone_otp,
        function='PHONE_VERIFICATION'
    )
    ## SENDING OTP TO THE USER
    send_email_otp(
        receiver=email,
        user_name=name['f_name'],
        otp=email_otp,
        function='EMAIL_VERIFICATION'
    )
    ## SENDING SMS OTP TO THE USER
    send_sms_otp(
        receiver=phone_number,
        user_name=name['f_name'],
        otp=phone_otp,
        function='PHONE_VERIFICATION'
    )

    return jsonify({
        'status':200,
        'msg':'provisional account created successfully, please verify your email and phone number.'
    })

@app.route('/student/verify_email',methods=['POST'])
def student_verify_email():
    ## THIS ROUTE INPUTS JSON VALUES THROUGH POST REQUEST 
    ## {
    ##   "enrollment": <STRING>,
    ##   "email_id": <STRING>,
    ##   "phone_number": <STRING>,
    ##   "email_otp": <INTEGER>
    ## }
    req = request.get_json()
    ## FETCHING EMAIL_OTP STORED IN THE DATABASE FOR VERIFICATION
    otp_db = db.OTP()
    hash_id = hash( req['enrollment'] + req['email_id'] + req['phone_number'])
    db_res = otp_db.query('hash_id',hash_id)
    if db_res['status'] == 212:
        for document in db_res['res']:
            if document['function'] == 'EMAIL_VERIFICATION':
                if int(document['otp']) == req['email_otp'] :
                    ## UPDATING PROVISIONAL_STUDENT_DB AND VALIDATING EMAIL ADDRESS PROVIDED BY USER
                    provisional_student = db.Provisional_Student()
                    provisional_student.update(hash_id,'email_verification_status',True)
                    ## REMOVING EMAIL VERIFICATION OTP FROM OTP_DB
                    otp_db.remove(hash_id,'EMAIL_VERIFICATION')
                    return jsonify({
                        'status':200,
                        'msg': 'email address validated successfully'
                    })
                else:
                    return jsonify({
                        'status':401,
                        'msg':'otp mismatch'
                    })
    return jsonify({
        'status':404,
        'msg':'otp not found in database, please try to regenerate otp'
    })


@app.route('/student/verify_phone',methods=['POST'])
def student_verify_phone():
    ## THIS ROUTE INPUTS JSON VALUES THROUGH POST REQUEST 
    ## {
    ##   "enrollment": <STRING>,
    ##   "email_id": <STRING>,
    ##   "phone_number": <STRING>,
    ##   "sms_otp": <INTEGER>
    ## }
    req = request.get_json()
    ## FETCHING EMAIL_OTP STORED IN THE DATABASE FOR VERIFICATION
    otp_db = db.OTP()
    hash_id = hash( req['enrollment'] + req['email_id'] + req['phone_number'])
    db_res = otp_db.query('hash_id',hash_id)
    if db_res['status'] == 212:
        for document in db_res['res']:
            if document['function'] == 'PHONE_VERIFICATION':
                if int(document['otp']) == req['sms_otp'] :
                    ## UPDATING PROVISIONAL_STUDENT_DB AND VALIDATING EMAIL ADDRESS PROVIDED BY USER
                    provisional_student = db.Provisional_Student()
                    provisional_student.update(hash_id,'phone_number_verification_status',True)
                    ## REMOVING EMAIL VERIFICATION OTP FROM OTP_DB
                    otp_db.remove(hash_id,'PHONE_VERIFICATION')
                    return jsonify({
                        'status':200,
                        'msg': 'phone number validated successfully'
                    })
                else:
                    return jsonify({
                        'status':401,
                        'msg':'otp mismatch'
                    })
    return jsonify({
        'status':404,
        'msg':'otp not found in database, please try to regenerate otp'
    })

@app.route("/student/login",methods=['POST'])
def student_authentication():
    user_credentials = request.get_json()
    student = db.Student()
    ## FETCHING PASSWORD FROM DATABASE FOR THE REQUESTED STUDENT ENROLLMENT
    db_res = student.query('enrollment',user_credentials['user_id'])
    if db_res['status'] == 212:         ## RUNS FOR SUCCESSFUL SEARCH OF ABOVE QUERY
        ## MATCHING REQ PASSWORD WITH DB PASSWORD
        for document in db_res['res']:
            if bcrypt.check_password_hash(document['password'],user_credentials['password']):
                ## JWT TOKEN GENERATION TAKES PLACE
                access_token = create_access_token(identity = user_credentials['user_id'])
                refresh_token = create_refresh_token(identity = user_credentials['user_id'])
                return jsonify({
                    'status':'200',
                    'access_token':access_token,
                    'refresh_token':refresh_token,
                    'msg':'login-successful'
                })
    return jsonify({'status':'401', 'msg':'Invalid UserId/Password'})

@app.route("/student/view_profile",methods=['POST'])
@jwt_required
def student_view_profile():
    ## THIS API IS USED TO VIEW ALL THE DETAILS OF A STUDENT STORED IN THE DATABASE.
    enrollment = get_jwt_identity()
    student = db.Student()
    db_res = student.query('enrollment',enrollment)
    if db_res['status']==212:
        for document in db_res['res']:            
            return jsonify({
                'enrollment': document['enrollment'],
                'rollno': document['rollno'],
                'name': document['name'],
                'phone_numbers': document['phone_numbers'],
                'email': document['email'],
                'father_name': document['father_name'],
                'year_of_join': document['year_of_join'],
                'year_of_pass': document['year_of_pass'],
                'programme': document['programme'],
                'branch': document['branch'],
                'section': document['section'],
                'gender': document['gender'],
                'dob': document['dob'],
                'temp_address': document['temp_address'],
                'perm_address': document['perm_address'] 
            })
    else:
        return jsonify({
            'status':db_res['status'],
            'msg':'Unsuccessful Search.'
        })

@app.route("/student/aboutus",methods=['POST'])
def student_aboutus():
    ## THIS ROUTE DOESN'T REQUIRE ANY JSON OR DATA FROM THE USER
    return jsonify({
        'developers':'the three musketers group',
        'msg':'for the community by the community',
        'status':'200'
    })
    
## ROUTE TO GENERATE OTP FOR A PARTICULAR USER ID
@app.route("/student/forgot_password/<user_id>",methods = ['GET'])
def student_forgot_password_generate_otp(user_id):
    ## INPUT IS ACCEPTED THROUGH URLENCODED VARIABLES I.E USER_ID
    ## CHECKING THE AVAILABILITY OF GIVEN USER_ID IN DATABASE
    student = db.Student()
    db_res = student.query('enrollment',user_id)
    if db_res['status'] == 212:
        otp_db = db.OTP()
        user_email_ids = []
        user_name = {}
        for res in db_res['res']:
            user_email_ids = res['email_ids']
            user_name = res['student_name']
        ## GENERATING OTP
        generated_otp = random.randrange(11111111,100000000)
        ## SENDING OTP TO THE USER THROUGH EMAIL
        send_email_otp(
            receiver = user_email_ids,
            user_name = user_name['f_name'],
            otp = generated_otp,
            function='RECOVER_PASSWORD'
        )
        ## INSERTING GENERATED OTP IN OTP_DB FOR AUTHORIZATION
        otp_db.insert(
            user_id = user_id,
            otp = generated_otp
        )
        ## MASKING EMAILS TO GENERATE REQUIRED RESPONSE
        for index in range(len(user_email_ids)):
            string = user_email_ids[index]
        ## MASKING STRING WITH 'X' AFTER FIRST 4 CHARACTERS AND BEFORE '@' SYMBOL
        string = string[:4] + 'X' * len(string[4:string.find('@')]) + string[string.find('@'):]
        user_email_ids[index] = string
        ## RETURNING RESPONSE
        return jsonify({
            'status':200,
            'msg':'otp sent to the registered email_ids',
            'email_ids':'user_email_ids'
        })
    else:
        return jsonify({
            'status':'206',
            'msg':'Invalid user_id'
        })

## ROUTE TO VIEW ATTENDANCE OF A STUDENT
@app.route('/student/view_attendance',methods=['POST'])
def student_view_attendance():
    attendance = db.Attendance('f026bpit', 'cryptocurrency', 'msc', 'it', 'b', '2022', '2')
    attendance.show_one('00320802717')
    return 'bleepbloop'

@app.route("/student/mark-attendance/subjects_list",methods=["GET"])
@jwt_required
def get_subjects_list():
    ## THIS API IS USED TO DISPLAY ALL THE SUBJECTS WITH THEIR FACULTY_ID OF THE TEACHER
    ## TEACHING THE SUBJECTS FOR A PARTICULAR ENROLLMENT NUMBER.
    req = request.get_json()
    semester = req["semester"]
    enrollment = get_jwt_identity()
    student = db.Student()
    student_query=student.query("enrollment",enrollment)
    if student_query["status"]==212:
        for res in student_query["res"]:
            programme = res["programme"]
            branch = res["branch"]
            section = res["section"]
            year_of_pass = res["year_of_pass"]
            my_collection = programme+'_'+branch+'_'+section+'_'+str(year_of_pass)+'_'+str(semester)
        attendance = db.Attendance('A0123','toc',programme,branch,section,year_of_pass,semester)
        db_res = attendance.show_collections()  
        for i in range(len(db_res)):
            db_res[i]=db_res[i].split('_')
        collection_name_db = []
        for i in range(len(db_res)):
            collection_name_db.append("_".join(db_res[i][2:]))
        result = []
        for i in range(len(collection_name_db)):
            if collection_name_db[i]==my_collection:
                result.append(db_res[i][0:2])
        return jsonify({
            'subjects': result,
            'msg':'All the subjects for the particular student has been successfully displayed.',
            'status':200 
        })
    else:
        return jsonify({
            'status':206,
            'msg':'invalid user id'
        })

@app.route("/student/mark-attendance/<faculty_id>/<subject>",methods=["POST"])
@jwt_required
def student_mark_attendance(faculty_id,subject):
    ## THIS API IS USED TO MARK ATTENDANCE OF A STUDENT WITH PARTICULAR ENROLLMENT NO.
    ## HE ENTERS THE OTP TOLD BY THE TEACHER.
    ## THE TEACHER VERIFIES THE OTP WITH THE OTP GENERATED IN HER PHONE.
    ## IF THE OTP IS VERIFIED, THE ATTENDANCE WILL BE MARKED. 
    enrollment = get_jwt_identity()  
    req=request.get_json()
    entered_otp=req["otp"]
    semester = req["semester"]
    otp = db.OTP() 
    student = db.Student()
    student_query=student.query("enrollment",enrollment)
    if student_query["status"]==212:
        for res in student_query["res"]:
            programme = res["programme"]
            branch = res["branch"]
            section = res["section"]
            year_of_pass = res["year_of_pass"] 
        attendance = db.Attendance(faculty_id,subject,programme,branch,section,year_of_pass,semester)
        date = datetime.now()
        time = datetime.now()
        day = date.strftime("%d")
        month = date.strftime("%m")
        year = date.strftime("%Y")
        hour = time.strftime("%H")
        mins = time.strftime("%M")
        date = {'day':day, 'month':month, 'year':year}
        time = str(hour) + ":" + str(mins)
        batch = db.Batch(programme,branch,section,year_of_pass)
        batch_output = batch.show_all()
        enrollment_dict = {}
        date_attendance = attendance.show_on(date,time)
        if date_attendance["status"] == 404:            
            for i in batch_output["res"]:
                enrollment_dict[i["enrollment"]]='a'
            attendance_dictionary = {
                'date': date,
                'time' : time,
                'attendance': enrollment_dict
            }  
            attendance.insert(attendance_dictionary)                            
        res = otp.query('user_id',faculty_id)  
        for i in res["res"]:
            otp_in_db = i["otp"]    
        if entered_otp == otp_in_db:
            show_attendance = attendance.show_on(date,time)
            for attendance_dictionary in show_attendance["res"]:
                attendance_dictionary["attendance"][enrollment]='p'
            attendance.update(date,time,attendance_dictionary)                
            return jsonify({
                "msg":"Attendance marked successfully.",
                'status':200                
            })
        else:
            return jsonify({
                'msg':" Please enter correct otp.",
            })
    else:
        return jsonify({
        'status':206,
        'msg':'invalid user id'
    })
    


if __name__ == '__main__':
    os.system(f"export PYTHONHASHSEED=0")
    app.run(debug=True,port=5000,host="0.0.0.0")
    