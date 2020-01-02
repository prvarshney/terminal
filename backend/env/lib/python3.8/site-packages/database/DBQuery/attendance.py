from pymongo import MongoClient
import sys
import config
from logger import log

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
		self._faculty_id = faculty_id
		self._subject = subject
		self._programme = programme
		self._branch = branch 
		self._section = section
		self._year_of_pass = year_of_pass
		self._semester = semester
		try:
			self.client = MongoClient(config.MongoDB_URI)
			self.db = self.client[config.Attendance_DB]
			log(f'[  INFO  ] {config.Attendance_DB} Connected Successfully')
		except:
			log('[ ERROR  ] Unable To Create Connection With Attendance_DB')
		# CREATING A COLLECTION IN DATABASE WITH IDENTIFIER LIKE
		# F45A_JAVA_BTECH_CSE_A_2021_5
		# THIS COLLECTION OBJECT IS GONNA BE USED FURTHER FOR ANY OPERATION LIKE :-
		# MARKING ATTENDANCE, SHOW, ETC.
		#
		self.collection = self.db[f'{faculty_id}_{subject}_{programme}_{branch}_{section}_{year_of_pass}_{semester}']

	def show_collections(self):
		# THIS FUNCTION RETURNS THE NAME OF ALL THE COLLECTION NAMES OF THE ATTENDANCE DB.
		return(self.db.collection_names())

	def insert(self,attendance_dictionary):
		# ATTENDANCE_DICTIONARY OBJECT CONTAINS A DICTIONARY, THAT STORES DATE ON WHICH ATTENDANCE
		# TAKEN AND THE PRESENT STATUS OF STUDENTS WITH THEIR ENROLLMENT NUMBER
		# ------------------------------------------------------------------------------------
		# FOR EXAMPLE :
		# ATTENDANCE_DICTIONARY = {
		#						'DATE':	{ 'DAY':04,'MONTH':06,'YEAR':1998 },
		#						'TIME' : 8 HOURS
		#						'ATTENDANCE': {
		#								'03620802717':'P',         # HERE P STANDS FOR PRESENT
		#								'03720802717':'A',		   # HERE A STANDS FOR ABSENT
		#								'05520802717':'P'
		#							}
		#						}
		#
		try:
			status = self.collection.insert_one(attendance_dictionary)
			log(f'[  INFO  ] {status}') 	# PRINTING STATUS OF RESULT OF QUERY
			log(f'[  INFO  ] Inserted {attendance_dictionary} at {self._faculty_id}_{self._subject}_{self._programme}_{self._branch}_{self._section}_{self._year_of_pass}_{self._semester} Collection Successfully in {config.Attendance_DB}')
			return 201
		except:
			log(f'[ ERROR  ] Insertion Of {attendance_dictionary} Operation Failed in {self._faculty_id}_{self._subject}_{self._programme}_{self._branch}_{self._section}_{self._year_of_pass}_{self._semester} Collection in {config.Attendance_DB}')
			return 417

	def show_all(self):
		# THIS METHOD DOESN'T INPUTS ANY PARAMETER AND RETURNS THE LIST OF ALL THE AVAILABLE
		# DOCUMENTS INSIDE COLLECTION FOR WHICH ATTENDANCE CONSTRUCTOR IS INITIALISED
		#
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
					'res':None
				}
			log(f'[  INFO  ] Attendence from {self._faculty_id}_{self._subject}_{self._programme}_{self._branch}_{self._section}_{self._year_of_pass}_{self._semester} Collection Fetched From {config.Attendance_DB}.')
		except:
			response = {
				'status':598,
				'res':None
			}
			log(f'[ ERROR  ] Unable To Fetch Attendence from {self._faculty_id}_{self._subject}_{self._programme}_{self._branch}_{self._section}_{self._year_of_pass}_{self._semester} Collection From {config.Attendance_DB}.')
		return response

	def show_on(self,query_date,query_time):
		# THIS METHOD INPUTS DATE DICTIONARY AND RETURNS LIST OF ATTENDANCE ON THAT
		# PARTICULAR DATE
		# ------------------------------------------------------------------------------------
		# DATA STRUCTURES OF INPUT PARAMETER :-
		# QUERY_DATE --> DICTIONARY
		#QUERY_TIME --> STRING
		#
		try:
			res = self.collection.find({ 'date': query_date ,'time':query_time})
			if res.count() > 0:
				response = {
					'status':202,
					'res':res
				}
			else:
				response = {
					'status':404,
					'res':None
				}
			log(f'[  INFO  ] Attendance Of {query_date} Date Fetched From {self._faculty_id}_{self._subject}_{self._programme}_{self._branch}_{self._section}_{self._year_of_pass}_{self._semester} Collection In {config.Attendance_DB}. ')
		except:
			response = {
				'status':598,
				'res':None
			}
			log(f'[ ERROR  ] Unable To Fetch Attendance Of a {query_date} Date Fetched From {self._faculty_id}_{self._branch}_{self._section}_{self._year_of_pass}_{self._semester} Collection In {config.Attendance_DB}. ')
		return response

	def remove_all(self):
		# THIS METHOD REMOVES THE COLLECTION OF ATTENDANCE OF THAT PARTICULAR FACULTY_ID FOR
		# WHICH CLASS OBJECT IS INTIALISED.
		#
		try:
			self.collection.drop()
			log(f'[  INFO  ] {self._faculty_id}_{self._subject}_{self._programme}_{self._branch}_{self._section}_{self._year_of_pass}_{self._semester} Collection Dropped Successfully from {config.Attendance_DB}.')
			return 512
		except:
			log(f'[ ERROR  ] Unable To Drop {self._faculty_id}_{self._subject}_{self._programme}_{self._branch}_{self._section}_{self._year_of_pass}_{self._semester} Collection from Attendance_DB.')
			return 400

	def show_one(self,enrollment):
		db_res = self.show_all()
		if db_res['status'] == 302:
			for document in db_res['res']:
				print(document['attendance'])

	def update(self,date,time,attendance_dictionary):
		# THIS METHOD USE TO UPDATE ATTENDANCE OF A PARTICULAR DATE WITH ATTENDANCE_DICTIONARY
		# OBJECT
		# ----------------------------------------------------------------------------------
		# DATA STRUCTURES OF INPUT PARAMETERS :-
		# DATE --> DICTIONARY
		# TIME --> STRING
		# ATTENDANCE_DICTIONARY --> DICTIONARY
		#
		searching_values = { 'date':date , 'time' :time}
		updation_value = attendance_dictionary
		try:
			status = self.collection.update_many(searching_values, {'$set':updation_value})
			log(f'[  INFO  ] {status}')
			log(f'[  INFO  ] Attendance Of {date} Updated Successfully as {attendance_dictionary}in {self._faculty_id}_{self._subject}_{self._programme}_{self._branch}_{self._section}_{self._year_of_pass}_{self._semester} Collection In {config.Attendance_DB}. ')					
			return 301
		except:
			log(f'[ ERROR  ] Unable To Update Attendance Of {date} in {self._faculty_id}_{self._subject}_{self._programme}_{self._branch}_{self._section}_{self._year_of_pass}_{self._semester} Collection In {config.Attendance_DB}.')
			return 204

	def __del__(self):
		# THIS DESTRUCTOR CLOSES CONNECTION OPENED BY THE OBJECT OF THIS CLASS
		self.client.close()


if __name__ == "__main__":
	# TESTING SCRIPT
	pass
