from pymongo import MongoClient
import sys
import config


## START OF ATTENDANCE COLLECTION API
## --------------------------------------------------------------------------
## THIS ATTENDANCE CLASS IS USED FOR THE FOLLOWING FUNCTIONS:-
## 1. MARKING ATTENDANCE WITH METHOD NAME - INSERT
## 2. SHOW WHOLE ATTENDANCE COLLECTION WITH METHOD NAME - SHOW_ALL
## 3. SHOW ATTENDANCE OF ANY PARTICULAR DATE WITH METHOD NAME - SHOW_ON
## 4. REMOVE ATTENDANCE COLLECTION WITH METHOD NAME - REMOVE_ALL
## 5. UPDATE ATTENDANCE OF ANY PARTICULAR DATE WITH METHOD NAME - UPDATE
##
class Attendance:
	def __init__(self,faculty_id,subject,programme,branch,section,year_of_pass,semester):
		# CONSTRUCTOR OF ATTENDANCE ACCEPTS THE FOLLOWING PARAMETERS :
		# FACULTY_ID --> UNIQUE_ID OF FACULTY --> STRING
		# SUBJECT --> STRING
		# PROGRAMME --> PROGRAMME OF CLASS WHOSE ATTENDANCE NEEDS TO MARK LIKE BBA, BTECH --> STRING
		# BRANCH --> LIKE CSE, ECE, ETC. --> STRING
		# SECTION --> STRING
		# YEAR_OF_PASS --> STRING
		# SEMESTER --> STRING
		#
		# CREATING CLIENT OF MONGODB SERVER
		try:
			self.client = MongoClient(config.MongoDB_URI)
			db = self.client[config.Attendance_DB]
		except:
			sys.exit(0)
		# CREATING A COLLECTION IN DATABASE WITH IDENTIFIER LIKE
		# F45A_JAVA_BTECH_CSE_A_2021_5
		# THIS COLLECTION OBJECT IS GONNA BE USED FURTHER FOR ANY OPERATION LIKE :-
		# MARKING ATTENDANCE, SHOW, ETC.
		#
		self.collection = db[f'{faculty_id}_{subject}_{programme}_{branch}_{section}_{year_of_pass}_{semester}']

	def insert(self,attendance_dictionary):
		# ATTENDANCE_DICTIONARY OBJECT CONTAINS A DICTIONARY, THAT STORES DATE ON WHICH ATTENDANCE
		# TAKEN AND THE PRESENT STATUS OF STUDENTS WITH THEIR ENROLLMENT NUMBER
		# ------------------------------------------------------------------------------------
		# FOR EXAMPLE :
		# ATTENDANCE_DICTIONARY = {
		#						'DATE':	{ 'DAY':04,'MONTH':06,'YEAR':1998 },
		#						'ATTENDANCE': {
		#								'03620802717':'P',         # HERE P STANDS FOR PRESENT
		#								'03720802717':'A',		   # HERE A STANDS FOR ABSENT
		#								'05520802717':'P'
		#							}
		#						}
		#
		try:
			status = self.collection.insert_one(attendance_dictionary)
			return 201
		except:
			return 417

	def show_all(self):
		# THIS METHOD DOESN'T INPUTS ANY PARAMETER AND RETURNS THE LIST OF ALL THE AVAILABLE
		# DOCUMENTS INSIDE COLLECTION FOR WHICH ATTENDANCE CONSTRUCTOR IS INITIALISED
		#
		try:
			res = list(self.collection.find({}))
			response = {
				'status':'302',
				'res':res
			}
		except:
			response = {
				'status':'598',
				'res':{}
			}
		return response

	def show_on(self,query_date):
		# THIS METHOD INPUTS DATE DICTIONARY AND RETURNS LIST OF ATTENDANCE ON THAT
		# PARTICULAR DATE
		# ------------------------------------------------------------------------------------
		# DATA STRUCTURES OF INPUT PARAMETER :-
		# QUERY_DATE --> DICTIONARY
		#
		try:
			res = list(self.collection.find({ 'date': query_date }))
			response = {
				'status':'202',
				'res':res
			}
		except:
			response = {
				'status':'404',
				'res':{}
			}
		return response

	def remove_all(self):
		# THIS METHOD REMOVES THE COLLECTION OF ATTENDANCE OF THAT PARTICULAR FACULTY_ID FOR
		# WHICH CLASS OBJECT IS INTIALISED.
		#
		try:
			self.collection.drop()
			return 512
		except:
			return 400

	def update(self,date,attendance_dictionary):
		# THIS METHOD USE TO UPDATE ATTENDANCE OF A PARTICULAR DATE WITH ATTENDANCE_DICTIONARY
		# OBJECT
		# ----------------------------------------------------------------------------------
		# DATA STRUCTURES OF INPUT PARAMETERS :-
		# DATE --> DICTIONARY
		# ATTENDANCE_DICTIONARY --> DICTIONARY
		#
		searching_values = { 'date':date }
		updation_value = attendance_dictionary
		try:
			status = self.collection.update_many(searching_values, {'$set':updation_value})
			return 301
		except:
			return 204

	def __del__(self):
		# THIS DESTRUCTOR CLOSES CONNECTION OPENED BY THE OBJECT OF THIS CLASS
		self.client.close()


if __name__ == "__main__":
	# TESTING SCRIPT
	pass
