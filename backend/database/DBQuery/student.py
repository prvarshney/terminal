from pymongo import MongoClient
from logger import log
import sys
import config
from flask_bcrypt import Bcrypt

## START OF STUDENT'S PROFILE COLLECTION API
## --------------------------------------------------------------------------
## THIS STUDENT PROFILE CLASS IS USED FOR THE FOLLOWING FUNCTIONS:-
## 1. INSERTING STUDENT PROFILE WITH METHOD NAME - INSERT
## 2. DELETING STUDENT PROFILE WITH METHOD NAME - DELETE
## 3. QUERYING STUDENT PROFILE WITH METHOD NAME - QUERY
## 4. UPDATE STUDENT PROFILE WITH METHOD NAME - UPDATE
##
class Student:
	def __init__(self):
		try:
			self.client = MongoClient(config.MongoDB_URI)
			db = self.client[config.Student_DB]
			log(f'[  INFO  ] {config.Student_DB} Connected Successfully')
		except:
			log(f'[  ERROR ] Unable To Create Connection With {config.Student_DB}')
		self.collection = db[config.Student_Profile_Collection]

	def insert(self, enrollment,rollno, name, phone_numbers, email,password, father_name, year_of_join,year_of_pass,
	 programme,branch, section, gender, dob, temp_address, perm_address):
		# THIS INSERT METHOD INPUTS NECESSARY DETAILS OF STUDENT THROUGH INPUT
		# PARAMETERS AND THEN INSERTS IT INTO DATABASE IF IT IS NOT PRESENT IN DB.
		#
		# DATA STRUCTURE OF INPUT PARAMETERS:-
		# ENROLLMENT --> STRING
		# ROLLNO --> INTEGER
		# NAME --> DICTIONARY
		# DOB --> DICTIONARY
		# PHONE_NUMBERS --> LIST OF STRING
		# EMAIL --> LIST OF STRING
		# PASSWORD --> HASHED STRING
		# FATHER_NAME --> DICTIONARY
		# YEAR_OF_JOIN --> INTEGER
		# YEAR_OF_PASS --> INTEGER
		# BRANCH --> STRING
		# SECTION --> STRING
		# GENDER --> STRING
		# TEMP_ADDRESS --> STRING
		# PERM_ADDRESS --> STRING
		#
		# IMPORTANT POINTS:-
		# 1. ENROLLMENT IS THE PRIMARY KEY FOR THE STUDENTS PROFILE COLLECTION.
		# 2. COLLECTION NAME THAT IS GOING TO BE USED IS : STUDENT_PROFILE
		# 3. PASSWORD SHOULD BE ENCRYPTED FIRST BEFORE STORING IN DATABASE.
		#
		# CREATING DICTIONARY OF THE DOCUMENT THAT IS GOING TO INSERT IN DB.
		bcrypt = Bcrypt()
		document = {
				"enrollment": enrollment,
				"rollno": rollno,
				"name": name,
				"phone_numbers": phone_numbers,
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
				"perm_address": perm_address
			}
		# CHECKING WHETHER ANY STUDENT IS ALREADY PRESENT IN DATABASE WITH SAME ENROLLMENT
		duplicate_entry = self.collection.find_one({ 'enrollment':enrollment })
		if duplicate_entry != None:
			log(f'[  ERROR ] Enrollment - {enrollment} Insertion at {config.Student_Profile_Collection} Collection in {config.Student_DB} failed - Duplicate Entry Found')
			return 417
		else:
			status = self.collection.insert_one(document)
			log(f'[  INFO  ] {status}') 	# PRINTING STATUS OF RESULT OF QUERY
			log(f'[  ERROR ] Enrollment - {enrollment} Successfully Inserted at {config.Student_Profile_Collection} Collection in {config.Student_DB}')
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
			log(f'[  INFO  ] The Search Query With {query_parameter}:{query_value} Accomplished Successfully in {config.Student_DB}')
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
			log(f'[  INFO  ] Enrollment - {enrollment} Removed From {config.Student_Profile_Collection} Collection in {config.Student_DB}')
			return 220
		except:
			return 203

	def update(self,enrollment,updation_param,updation_value):
		# THIS UPDATE FUNCTION INPUTS THE ENROLLMENT, TO CHECK WHICH DOCUMENT NEEDS TO UPDATE
		# AND THEN, UPDATES THE UPDATION_PARAM WITH UPDATION_VALUE.
		# --------------------------------------------------------------------------------------
		# DATA STRUCTURES OF INPUT PARAMETERS :-
		# ENROLLMENT --> STRING
		# UPDATION_PARAM --> STRING
		# UPDATION_VALUE --> STRING, LIST, DICTIONARY
		#
		searching_values = {'enrollment':enrollment}
		updating_values = { updation_param:updation_value }
		try:
			status = self.collection.update_one(searching_values, {'$set':updating_values})
			log(f'[  INFO  ] {status}')
			log(f'[  INFO  ] Enrollment - {enrollment} Updated With - {updation_param}:{updation_value} in {config.Student_DB}')
			return 301
		except:
			log(f'[  ERROR ] Failed to Update Enrollment - {enrollment} With - {updation_param}:{updation_value} in {config.Student_DB}')
			return 204

	def __del__(self):
		self.client.close()

if __name__ == "__main__":
	# TEST CODE COMES HERE
	pass
