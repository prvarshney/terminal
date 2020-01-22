from pymongo import MongoClient
from logger import log
import sys
import config
from flask_bcrypt import Bcrypt

## START OF PROVISIONAL STUDENT'S PROFILE COLLECTION API
## --------------------------------------------------------------------------
## THIS PROVISIONAL STUDENT PROFILE CLASS IS USED FOR THE FOLLOWING FUNCTIONS:-
## 1. INSERTING PROVISIONAL STUDENT PROFILE WITH METHOD NAME - INSERT
## 2. DELETING PROVISIONAL STUDENT PROFILE WITH METHOD NAME - DELETE
## 3. QUERYING PROVISIONAL STUDENT PROFILE WITH METHOD NAME - QUERY
## 4. UPDATE PROVISIONAL STUDENT PROFILE WITH METHOD NAME - UPDATE
##
class Provisional_Student:
    def __init__(self):
        try:
            self.client = MongoClient(config.MongoDB_URI)
            db = self.client[config.Provisional_Student_DB]
            log(f'[  INFO  ] {config.Provisional_Student_DB} Connected Successfully')
        except:
            log(f'[  ERROR ] Unable To Create Connection With {config.Provisional_Student_DB}')
        self.collection = db[config.Student_Profile_Collection]

    def insert(self ,enrollment,rollno, name, phone_number, email,password, father_name, year_of_join,year_of_pass,programme,branch, section, gender, dob,
     temp_address, perm_address, identity_proof, phone_number_verification_status=False,email_verification_status=False):
        # THIS INSERT METHOD INPUTS NECESSARY DETAILS OF STUDENT THROUGH INPUT
        # PARAMETERS AND THEN INSERTS IT INTO DATABASE IF IT IS NOT PRESENT IN DB.
        #
        # DATA STRUCTURE OF INPUT PARAMETERS:-
        # ENROLLMENT --> STRING
        # ROLLNO --> INTEGER
        # NAME --> DICTIONARY
        # DOB --> DICTIONARY
        # PHONE_NUMBER --> STRING
        # EMAIL --> STRING
        # PASSWORD --> HASHED STRING
        # FATHER_NAME --> DICTIONARY
        # YEAR_OF_JOIN --> INTEGER
        # YEAR_OF_PASS --> INTEGER
        # PROGRAMME --> STRING
        # BRANCH --> STRING
        # SECTION --> STRING
        # GENDER --> STRING
        # DOB --> DICTIONARY
        # TEMP_ADDRESS --> STRING
        # PERM_ADDRESS --> STRING
        # IDENTITY_PROOF --> STRING
        # PHONE_NUMBER_VERIFICATION_STATUS --> BOOLEAN
        # EMAIL_VERIFICATION_STATUS --> BOOLEAN
        #
        # IMPORTANT POINTS:-
        # 1. ENROLLMENT IS THE PRIMARY KEY FOR THE STUDENTS PROFILE COLLECTION.
        # 2. COLLECTION NAME THAT IS GOING TO BE USED IS : STUDENT_PROFILE
        # 3. PASSWORD SHOULD BE ENCRYPTED FIRST BEFORE STORING IN DATABASE.
        #
        # CREATING DICTIONARY OF THE DOCUMENT THAT IS GOING TO INSERT IN DB.
        bcrypt = Bcrypt()
        hash_id = hash( str(enrollment) + str(email) +str(phone_number) )
        # CHECKING THE PRESENCE OF DUPLICATE ENTRY IN DATABASE
        res = self.collection.find({ 'hash_id': hash_id })
        if res.count() > 0:
            log(f'[  INFO  ] For Hash ID - {hash_id} Duplicate Entry Found at {config.Provisional_Student_Profile_Collection} Collection in {config.Provisional_Student_DB}')
            status = self.collection.delete_many({ 'hash_id':hash_id })
            log(f'[  INFO  ] {status}')
            log(f'[  INFO  ] Hash_ID - {hash_id} Removed Successfully from {config.Provisional_Student_Profile_Collection} Collection in {config.Provisional_Student_DB}')
        document = {
                "hash_id": hash_id,
                "enrollment": enrollment,
                "rollno": rollno,
                "name": name,
                "phone_number": phone_number,
                "email": email,
                "password": bcrypt.generate_password_hash(password).decode('utf-8'),
                "father_name": father_name,
                "year_of_join": year_of_join,
                "year_of_pass": year_of_pass,
                "programme": programme,
                "branch": branch,
                "section": section,
                "gender": gender,
                "dob": dob,
                "temp_address": temp_address,
                "perm_address": perm_address,
                "identity_proof":identity_proof,
                "phone_number_verification_status":phone_number_verification_status,
                "email_verification_status":email_verification_status
            }
        status = self.collection.insert_one(document)
        log(f'[  INFO  ] {status}') 	# PRINTING STATUS OF RESULT OF QUERY
        log(f'[  INFO  ] Enrollment - {enrollment} Successfully Inserted at {config.Student_Profile_Collection} Collection in {config.Provisional_Student_DB}')
        return 201

    def query(self,query_parameter,query_value):
        # THIS QUERY FUNCTION INPUTS QUERY PARAMETER LIKE ENROLLMENT_ID, NAME, ETC. AND QUERY VALUE
        # TO SEARCH DOCUMENTS IN COLLECTION. AFTER SUCCESSFUL SEARCH IT RETURNS
        # REST OF THE DETAILS TO THE USER.
        # ---------------------------------------------------------------------------------
        # DATA STRUCTURES OF INPUT PARAMETERS :-
        # QUERY_PARAMETER --> STRING
        # QUERY_VALUE --> STRING, DICTIONARY, LIST OF STRING
        #
        try:
            res = self.collection.find({ query_parameter:query_value })
            log(f'[  INFO  ] The Search Query With {query_parameter}:{query_value} Accomplished Successfully in {config.Provisional_Student_DB}')
            if res.count() > 0:
                response = {
                    'status':212,
                    'res': res
                }
            else:
                response = {
                    'status':212,
                    'res': {}
                }
        except:
            response = {
                'status':206,
                'res':None
            }
        return response

    def remove(self,query_parameter,query_value):
        # THIS FUNCTION REMOVES THOSE DOCUMENTS WHICH POSSESS QUERY_PARAMETER AS ANY KEY
        # AND QUERY_VALUE AS THEIR VALUES FROM COLLECTION
        #------------------------------------------------------------------------------------
        # DATA STRUCTURES OF INPUT PARAMETERS :-
        # QUERY_PARAMETER --> STRING
        # QUERY_VALUE --> LIST, STRING, DICTIONARY
        #
        try:
            status = self.collection.delete_many({ query_parameter:query_value })
            log(f'[  INFO  ] {status}')
            log(f'[  INFO  ] Enrollment - {enrollment} Removed From {config.Student_Profile_Collection} Collection in {config.Provisional_Student_DB}')
            return 220
        except:
            return 203

    def update(self,hash_id,updation_param,updation_value):
        # THIS UPDATE FUNCTION INPUTS THE hash_id, TO CHECK WHICH DOCUMENT NEEDS TO UPDATE
        # AND THEN, UPDATES THE UPDATION_PARAM WITH UPDATION_VALUE.
        # --------------------------------------------------------------------------------------
        # DATA STRUCTURES OF INPUT PARAMETERS :-
        # hash_id --> STRING
        # UPDATION_PARAM --> STRING
        # UPDATION_VALUE --> STRING, LIST, DICTIONARY
        #
        searching_values = {'hash_id':hash_id}
        updating_values = { updation_param:updation_value }
        try:
            status = self.collection.update_one(searching_values, {'$set':updating_values})
            log(f'[  INFO  ] {status}')
            log(f'[  INFO  ] Hash_ID - {hash_id} Updated With - {updation_param}:{updation_value} in {config.Provisional_Student_DB}')
            return 301
        except:
            log(f'[  ERROR ] Failed to Update Hash_ID - {hash_id} With - {updation_param}:{updation_value} in {config.Provisional_Student_DB}')
            return 204

    def show_all(self):
        # USED TO DISPLAY A LIST OF ALL THE ENROLLED STUDENTS IN A CLASS
        try:
            res = self.collection.find({})
            if res.count() > 0:
                response = {
                    'status':302,
                    'res':res
                }
            else:
                response = {
                    'status':302,
                    'res':{}
                }
            log('[  INFO  ] Provisional Student Database Collection Fetched From Batch_DB')
        except:
            response = {
                'status':598,
                'res':None
            }
            log(f'[  ERROR ] Unable To Fetch Provisonal Student Database Collection From Batch_DB')
        return response

    def __del__(self):
        self.client.close()

if __name__ == "__main__":
	# TEST CODE COMES HERE
	pass
