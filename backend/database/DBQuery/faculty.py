from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import config
import sys
from logger import log

## START OF FACULTY'S PROFILE COLLECTION API
## --------------------------------------------------------------------------
## THIS FACULTY CLASS USED FOR THE FOLLOWING FUNCTIONS :
## 1. INSERTING FACULTY PROFILE WITH METHOD NAME - INSERT
## 2. DELETING FACULTY PROFILE WITH METHOD NAME - REMOVE
## 3. QUERYING FACULTY PROFILE WITH METHOD NAME - QUERY
## 4. UPDATE FACULTY PROFILE WITH METHOD NAME - UPDATE
##
class Faculty:
	def __init__(self):
		try:
			self.client = MongoClient(config.MongoDB_URI)
			db = self.client[config.Faculty_DB]
			log('[ INFO  ] Faculty_DB connected successfully')
		except:
			log('[ Error ] Unable to create connection with Faculty_DB')
			sys.exit(0)
		self.collection = db[config.Faculty_Profile_Collection]

	def insert(self,id,name,dob,phone_numbers,email,password,subjects,qualifications=[],
		time_table={},classes=[],ratings=5):
		# THIS INSERT METHOD INPUTS NECESSARY DETAILS OF FACULTY THROUGH
		# INPUT PARAMETERS AND THEN INSERT IT INTO DATABASE IF IT DOESN'T PRESENTS IN DB
		#--------------------------------------------------------------------------------
		# DATASTRUCTURE OF INPUT PARAMETERS :
		# ID --> STRING
		# NAME --> DICTIONARY
		# DOB --> DICTIONARY
		# PHONE NUMBERS --> LIST OF STRING
		# EMAIL --> LIST OF STRING
		# PASSWORD --> STRING OF HASH
		# SUBJECTS --> LIST OF STRING
		# QUALIFICATIONS --> LIST OF STRING
		# TIMETABLE --> DICTIONARY
		# CLASSES --> LIST OF STRING
		# RATINGS --> STRING
		#
		# IMPORTANT POINTS :
		# 	*QUALIFICATIONS, TIME-TABLE, CLASSES, RATINGS, REVIEWS ARE OPTIONAL PARAMETERS IF NOT
		# 	 PROVIDED DEFAULT VALUES ARE USED
		# 	*ID IS THE PRIMARY KEY FOR FACULTY PROFILE COLLECTIONS
		# 	*COLLECTION NAME THAT IS GOING TO BE USED : FACULTY_PROFILE
		#	*ALWAYS STORE PASSWORD IN ENCRYPTED FORM IN ORDER TO PROTECT USER'S PASSWORDS
		#
		# CREATING DICTIONARY OF THE DOCUMENT THAT IS REQUIRED TO INSERT IN DB
		bcrypt = Bcrypt()
		document = {
				"faculty_id":id,
				"name":name,
				"date_of_birth":dob,
				"phone_numbers":phone_numbers,
				"email":email,
				"password":bcrypt.generate_password_hash(password).decode('utf-8'),
				"subjects":subjects,
				"qualifications":qualifications,
				"time-table":time_table,
				"classes":classes,
				"ratings":ratings,
				}
		# CHECKING WHETHER ANY FACULTY WITH SAME FACULTY_ID IS PRESENT IN DATABASE
		duplicate_entry = self.collection.find_one({ 'faculty_id':id })
		if duplicate_entry != None:		# RUN WHEN THEIR PRESENTS ANY DUPLICATE FACULTY_ID IN DB
			log('[ Error ] Object of this ID already present in database')
			return 417
		else:			# RUNS WHEN THERE DOESN'T PRESENT ANY DUPLICATE ENTRY
			status = self.collection.insert_one(document)
			log(f'[ INFO  ] {status}') 	# PRINTING STATUS OF RESULT OF QUERY
			log('[ INFO  ] A faculty has been inserted in Faculty_DB.')
			return 201

	def query(self,query_parameter,query_value):
		# THIS QUERY FUNCTION INPUTS QUERY PARAMETER LIKE FACULTY_ID, NAME, ETC. AND QUERY VALUE
		# TO SEARCH DOCUMENTS IN COLLECTION. AFTER SUCCESSFUL SEARCH IT RETURNS
		# REST OF THE DETAILS TO THE USER.
		# -----------------------------------------------------------------------
		# DATA STRUCTURE OF INPUT PARAMETERS :-
		# QUERY_PARAMETER --> STRING
		# QUERY_VALUE --> STRING, DICTIONARY, LIST
		#
		try:
			res = self.collection.find({ query_parameter:query_value })
			response = {
				'status':212,
				'res': res
			}
		except:
			response = {
				'status':206,
				'res':res
			}
		log('[ INFO  ] The search query is successfully completed.')
		return response

	def remove(self,query_parameter,query_value):
		# THIS REMOVE FUNCTION DELETES THOSE DOCUMENTS FROM COLLECTION WHICH HAVE QUERY_PARAMETER
		# AS A KEY AND QUERY_VALUE AS A VALUE
		#----------------------------------------------------------------------------------
		# DATA STRUCTURES OF INPUT PARAMETERS :
		# QUERY_PARAMETER --> STRING
		# QUERY_VALUE --> STRING,DICTIONARY OR LIST
		#
		try:
			status = self.collection.delete_many({ query_parameter:query_value })
			log(f'[ INFO  ] {status}')
			log('[ INFO  ] The faculty with the given query has been successfully removed from Faculty_DB.')
			return 220
		except:
			return 203

	def update(self,faculty_id,updation_param,updation_value):
		# THIS UPDATE FUNCTION INPUTS THE FACULTY_ID TO CHECK WHICH DOCUMENT NEEDS TO UPDATE
		# AND THEN UPDATES THE UPDATION_PARAM WITH UPDATION_VALUE
		# ----------------------------------------------------------------------------------
		# DATA STRUCTURES OF INPUT PARAMETERS :
		# FACULTY_ID --> STRING
		# UPDATION_PARAM --> STRING
		# UPDATION VALUE --> FOR ID,RATINGS AS UPDATION_PARAM --> STRING
		#				 --> FOR NAME,DOB,TIMETABLE --> DICTIONARY
		#				 --> FOR PHONE_NUMBERS, EMAIL, SUBJECT, QUALIFICATION, CLASSES --> LIST OF STRING
		#
		searching_values = {'faculty_id':faculty_id }
		updating_values = { updation_param:updation_value }
		try:
			status = self.collection.update_one(searching_values, {'$set':updating_values})
			log(f'[ INFO  ] {status}')
			log(f'[ INFO  ] {faculty_id} Faculty_DB has been updated.')
			return 301
		except:
			log('[ ERROR  ] Updation failed.')
			return 204

	def __del__(self):
		self.client.close()


if __name__ == "__main__":
	# TEST CODE COMES HERE
	pass
