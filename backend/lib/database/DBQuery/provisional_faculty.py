from pymongo import MongoClient
from logger import log
import sys
import config
from flask_bcrypt import Bcrypt

## START OF PROVISIONAL FACULTY'S PROFILE COLLECTION API
## -------------------------------------------------------------------------
## THIS PROVISIONAL FACULTY PROFILE CLASS IS USED FOR THE FOLLOWING FUNCTIONS:-
## 1. INSERTING PROVISIONAL FACULTY PROFILE WITH METHOD NAME - INSERT
## 2. DELETING PROVISIONAL FACULTY PROFILE WITH METHOD NAME - DELETE
## 3. QUERYING PROVISIONAL FACULTY PROFILE WITH METHOD NAME - QUERY
## 4. UPDATE PROVISIONAL FACULTY PROFILE WITH METHOD NAME - UPDATE
##
class Provisional_Faculty:
    def __init__(self):
        try:
            self.client = MongoClient(config.MongoDB_URI)
            db = self.client[config.Provisional_Faculty_DB]
            log(f'[  INFO  ] {config.Provisional_Faculty_DB} Connected Successfully')
        except:
            log(f'[  ERROR ] Unable To Create Connection With {config.Provisional_Faculty_DB}')
        self.collection = db[config.Faculty_Profile_Collection]

    def insert(self, faculty_id, name, phone_number, email, password, dob, phone_number_verification_status = False, 
    email_verification_status=False):
        # THIS INSERT METHOD INPUTS NECESSARY DETAILS OF FACULTY THROUGH INPUT
        # PARAMETERS AND THEN INSERTS IT INTO DATABASE IF IT IS NOT PRESENT IN DB.
        #
        # DATA STRUCTURE OF INPUT PARAMETERS:-
        # FACULTY_ID --> STRING
        # NAME --> DICTIONARY
        # PHONE_NUMBER --> STRING
        # EMAIL --> STRING
        # PASSWORD --> HASHED STRING
        # DOB --> DICTIONARY
        # PHONE_NUMBER_VERIFICATION_STATUS --> BOOLEAN
        # EMAIL_VERIFICATION_STATUS --> BOOLEAN
        #
        # IMPORTANT POINTS :-
        # 1. FACULTY_ID IS THE PRIMARY KEY FOR THE FACULTY'S PROFILE COLLECTION.
        # 2. COLLECTION NAME THAT IS GOING TO BE USED IS : FACULTY_PROFILE.
        # 3. PASSWORD SHOULD BE ENCRYPTED FIRST BEFORE STORING IN DATABASE.
        #
        # CREATING DICTIONARY OF THE DOCUMENT THAT IS GOING TO INSERT IN DB.
        bcrypt = Bcrypt()
        hash_id = hash( str(faculty_id) + str(email) + str(phone_number) )
        # CHECKING THE PRESENCE OF DUPLICATE ENTRY IN DATABASE
        try:
            res = self.collection.find({ 'hash_id': hash_id})
            if res.count() > 0:
                log(f'[  INFO  ] For Hash ID - {hash_id} Duplicate Entry Found At Collection - {config.Faculty_Profile_Collection} In Database - {config.Provisional_Faculty_DB}')
                status  = self.collection.delete_many({ 'hash_id': hash_id })
                log(f'[  INFO  ] {status}')
                log(f'[  INFO  ] Hash_ID - {hash_id} Removed Successfully From Collection - {config.Faculty_Profile_Collection} In Database - {config.Provisional_Faculty_DB}')
            document = {
                    "hash_id": hash_id,
                    "faculty_id": faculty_id,
                    "name": name,
                    "phone_number": phone_number,
                    "email": email,
                    "password": bcrypt.generate_password_hash(password).decode('utf-8'),
                    "dob": dob,
                    "phone_number_verification_status": phone_number_verification_status,
                    "email_verification_status": email_verification_status
                }
            status = self.collection.insert_one(document)
            log(f'[  INFO  ] {status} ')                # PRINTING STATUS OF RESULT OF QUERY
            log(f'[  INFO  ] Faculty_ID - {faculty_id} Successfully Inserted at Collection - {config.Faculty_Profile_Collection} In Database - {config.Provisional_Faculty_DB}')
            return 201
        except:
            log(f'[  ERROR ] API Failed to insert Faculty_ID - {faculty_id} at Collection - {config.Faculty_Profile_Collection} In Database - {config.Provisional_Faculty_DB}')
            return 417

    def query(self,query_parameter,query_value):
        # THIS QUERY FUNCTION INPUTS QUERY PARAMETER LIKE FACULTY_ID, NAME, ETC. AND QUERY VALUE
        # TO SEARCH DOCUMENTS IN COLLECTION. AFTER SUCCESSFUL SEARCH IT RETURNS
        # REST OF THE DETAILS TO THE USER.
        # ---------------------------------------------------------------------------------
        # DATA STRUCTURES OF INPUT PARAMETERS :-
        # QUERY_PARAMETER --> STRING
        # QUERY_VALUE --> STRING, DICTIONARY, LIST OF STRING
        #        
        try:
            res = self.collection.find({ query_parameter:query_value })
            log(f'[  INFO  ] The Search Query With {query_parameter}:{query_value} Accomplished Successfully at Collection - {config.Faculty_Profile_Collection} In Database - {config.Provisional_Faculty_DB}')
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
            log(f'[  ERROR ] API Failed to Query {query_parameter}:{query_value} at Collection - {config.Faculty_Profile_Collection} In Database - {config.Provisional_Faculty_DB}')
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
            log(f'[  INFO  ] {query_parameter}:{query_value} Removed Successfully from Collection - {config.Faculty_Profile_Collection} In Database - {config.Provisional_Faculty_DB}')
            return 220
        except:
            log(f'[  ERROR ] API Failed to remove {query_parameter}:{query_value} from Collection - {config.Faculty_Profile_Collection} In Database - {config.Provisional_Faculty_DB}')
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
            log(f'[  INFO  ] Hash_ID - {hash_id} Updated With - {updation_param}:{updation_value} at Collection - {config.Faculty_Profile_Collection} In Database - {config.Provisional_Faculty_DB}')
            return 301
        except:
            log(f'[  ERROR ] API Failed to Update Hash_ID - {hash_id} With - {updation_param}:{updation_value} at Collection - {config.Faculty_Profile_Collection} In Database - {config.Provisional_Faculty_DB}')
            return 204

    def __del__(self):
        try:
            self.client.close()
            log(f'[  INFO  ] Closing Established Connection with Collection - {config.Faculty_Profile_Collection} In Database - {config.Provisional_Faculty_DB}')
        except:
            log(f'[  ERROR ] API failed while Closing Established Connection with Collection - {config.Faculty_Profile_Collection} In Database - {config.Provisional_Faculty_DB}')

if __name__ == "__main__":
	# TEST CODE COMES HERE
	pass
