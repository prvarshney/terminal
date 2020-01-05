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
			log(f'[  INFO  ] {config.Faculty_DB} Connected Successfully')
		except:
			log(f'[  ERROR ] Unable To Create Connection With {config.Faculty_DB}')
		self.collection = db[config.Faculty_Profile_Collection]

	def insert(self,id,name,dob,phone_number,email,password,subjects,qualifications=[],
		time_table={},classes=[],ratings=5):
		# THIS INSERT METHOD INPUTS NECESSARY DETAILS OF FACULTY THROUGH
		# INPUT PARAMETERS AND THEN INSERT IT INTO DATABASE IF IT DOESN'T PRESENTS IN DB
		#--------------------------------------------------------------------------------
		# DATASTRUCTURE OF INPUT PARAMETERS :
		# ID --> STRING
		# NAME --> DICTIONARY
		# DOB --> DICTIONARY
		# PHONE NUMBER --> STRING
		# EMAIL --> STRING
		# PASSWORD --> STRING OF HASH
		# SUBJECTS --> LIST OF STRING
		# QUALIFICATIONS --> LIST OF STRING
		# TIMETABLE --> DICTIONARY
		# CLASSES --> LIST OF STRING
		# RATINGS --> STRING
		#
		# TIMETABLE FORMAT :-
		# {
		#	'monday':{
		#			   '1015-1215':'btech_cse_a_2021',
		#			   '1400-1600':'btech_it_b_2022'
		# 			},
		#	'tuesday':{...},
		#	   ...	   ...,
		#	   ...	   ...,
		#	   ...	   ...,
		#	   ...	   ...,
		#	'sunday':{...}
		# } 
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
				"phone_number":phone_number,
				"email":email,
				"password":bcrypt.generate_password_hash(password).decode('utf-8'),
				"subjects":subjects,
				"qualifications":qualifications,
				"time-table":time_table,
				"classes":classes,
				"ratings":ratings
				}
		try:
			# CHECKING WHETHER ANY FACULTY WITH SAME FACULTY_ID IS PRESENT IN DATABASE
			duplicate_entry = self.collection.find_one({ 'faculty_id':id })
			if duplicate_entry != None:		# RUN WHEN THEIR PRESENTS ANY DUPLICATE FACULTY_ID IN DB
				log(f'[  ERROR ] Faculty - {id} Insertion at Collection - {config.Faculty_Profile_Collection} in Database - {config.Faculty_DB} failed - Duplicate Entry Found')
				return 417
			else:			# RUNS WHEN THERE DOESN'T PRESENT ANY DUPLICATE ENTRY
				status = self.collection.insert_one(document)
				log(f'[  INFO  ] {status}') 	# PRINTING STATUS OF RESULT OF QUERY
				log(f'[  INFO  ] Faculty - {id} Inserted at Collection - {config.Faculty_Profile_Collection} in Database - {config.Faculty_DB}')
				return 201
		except:
			log(f'[  ERROR ] API Failed to insert Faculty - {id} at Collection - {config.Faculty_Profile_Collection} in Database - {config.Faculty_DB}')			
			return 417

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
			if res.count() > 0:
				response = {
					'status':212,
					'res': res
				}
			else:
				response = {
					'status':206,
					'res':res
				}	
			log(f'[  INFO  ] The Search Query With {query_parameter}:{query_value} Accomplished Successfully at Collection - {config.Faculty_Profile_Collection} in Database - {config.Faculty_DB}')
		except:
			response = {
				'status':206,
				'res':res
			}
			log(f'[  ERROR ] API Failed to Query With {query_parameter}:{query_value} at Collection - {config.Faculty_Profile_Collection} in Database - {config.Faculty_DB}')
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
			log(f'[  INFO  ] {status}')
			log(f'[  INFO  ] Faculty - {query_parameter}:{query_value} Removed Successfully from {config.Faculty_DB}')
			return 220
		except:
			log(f'[ ERROR  ] API failed to remove Faculty - {query_parameter}:{query_value} from Collection - {config.Faculty_Profile_Collection} in Database - {config.Faculty_DB}')
			return 203

	def update(self,faculty_id,updation_param,updation_value):
		# THIS UPDATE FUNCTION INPUTS THE FACULTY_ID TO CHECK WHICH DOCUMENT NEEDS TO UPDATE
		# AND THEN UPDATES THE UPDATION_PARAM WITH UPDATION_VALUE
		# ----------------------------------------------------------------------------------
		# DATA STRUCTURES OF INPUT PARAMETERS :
		# FACULTY_ID --> STRING
		# UPDATION_PARAM --> STRING
		# UPDATION VALUE --> FOR ID,RATINGS, PHONE_NUMBER, EMAIL, AS UPDATION_PARAM --> STRING
		#				 --> FOR NAME,DOB,TIMETABLE --> DICTIONARY
		#				 --> FOR SUBJECT, QUALIFICATION, CLASSES --> LIST OF STRING
		#
		searching_values = {'faculty_id':faculty_id }
		updating_values = { updation_param:updation_value }
		try:
			status = self.collection.update_one(searching_values, {'$set':updating_values})
			log(f'[  INFO  ] {status}')
			log(f'[  INFO  ] Faculty - {faculty_id} Updated With - {updation_param}:{updation_value} in {config.Faculty_DB}')
			return 301
		except:
			log(f'[ ERROR  ] API failed while Updating Faculty - {faculty_id} With - {updation_param}:{updation_value} at Collection - {config.Faculty_Profile_Collection} in Database - {config.Faculty_DB}')
			return 204

	def __del__(self):
		try:
			self.client.close()
			log(f'[  INFO  ] Closing Established Connection with Collection - {config.Faculty_Profile_Collection} in Database - {config.Faculty_DB}')
		except:
			log(f'[  ERRROR ] API failed while Closing Established Connection with Collection - {config.Faculty_Profile_Collection} in Database - {config.Faculty_DB}')


if __name__ == "__main__":
	# TEST CODE COMES HERE
	pass
