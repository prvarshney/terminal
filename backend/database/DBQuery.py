# This module acts as an API for CRUD operations in database
from pymongo import MongoClient
import config
import sys

# Creating connection with the mongodb database
try:
	client = MongoClient(config.MongoDB_URI)        # Use this client object to query database
	db = client[config.Database_Name]               # Use this db object to query collections
except:
	print('[ Error ] Unable to create connection with Database')
	sys.exit(0)
## Start of Faculty's Profile Collection API
## --------------------------------------------------------------------------
## This faculty class used for the following functions :
## 1. Inserting faculty profile with method name - insert
## 2. Deleting faculty profile with method name - remove
## 3. Querying faculty profile with method name - query
## 4. Update faculty profile with method name - update

class faculty:
	def insert(self,id,name,dob,phone_numbers,email,subjects,qualifications=[],
		time_table={},classes=[],ratings=5,reviews=[]):
		# This insert method inputs necessary details of faculty through input parameters and then
		# insert it into database if it doesn't presents in DB
		#
		# Datastructure of input parameters :
		# id --> string
		# name --> dictionary
		# dob --> dictionary
		# phone numbers --> list of string
		# email --> list of string
		# subjects --> list of string
		# qualifications --> list of string
		# timetable --> dictionary
		# classes --> list of string
		# ratings --> float
		# reviews --> list of strings
		
		# Important Points :
		# 	*qualifications, time-table, classes, ratings, reviews are optional parameters if not
		# 	 provided default values are used
		# 	*id is the primary key for faculty profile collections
		# 	*collection name that is going to be used : faculty_profile

		# Creating dictionary of the document that is required to insert in DB
	    document = {
			    "faculty_id":id,
			    "name":name,
			    "date_of_birth":dob,
			    "phone_numbers":phone_numbers,
			    "email":email,
			    "subjects":subjects,
			    "qualifications":qualifications,
			    "time-table":time_table,
			    "classes":classes,
			    "ratings":ratings,
			    "reviews":reviews
	    		}

	    # Checking whether any faculty with same faculty_id is present in database
	    duplicate_entry = db[config.Faculty_Profile_Collection].find_one({ f'faculty_id':f'{id}' })
	    if duplicate_entry != None:
	    	print('[ Error ] Object of this ID already present in database')
	    	return False
	    else:
		    status = db[config.Faculty_Profile_Collection].insert_one(document)
		    print(f'[ INFO  ] {status}') 	# Printing Status of result of query
		    return True

	def query(self,query_parameter,query_value):
		# This query function inputs query parameter like faculty_id, name, etc. and query value
		# to search documents in collection. After successful search it returns
		# rest of the details to the user.
		return list(db[config.Faculty_Profile_Collection].find({ f'{query_parameter}':f'{query_value}' }))

	def remove(self,query_parameter,query_value):
		# This remove function inputs query parameter like faculty_id, name, etc. and query value
		# to search documents in collection. After that remove them from collection
		status = db[config.Faculty_Profile_Collection].delete_many({ f'{query_parameter}':f'{query_value}' })
		print(f'[ INFO  ] {status}')

	def update(self,faculty_id,updation_param,updation_value):
		searching_values = {'faculty_id':f'{faculty_id}'}
		updating_values = {f'{updation_param}':f'{updation_value}'}
		db[config.Faculty_Profile_Collection].update_one(searching_values, {'$set':updating_values})


## Start of Student's Profile Collection API
## --------------------------------------------------------------------------
## This student profile class is used for the following functions:-
## 1. Inserting student profile with method name - insert
## 2. Deleting student profile with method name - delete
## 3. Querying student profile with method name - query
## 4. Update student profile with method name - update

class student:
	def insert(self, enrollment, name, phone_numbers, email, father_name, year_of_join,year_of_pass,
	 programme,branch, section, gender, dob, temp_address, perm_address):
		# This insert method inputs necessary details of student through input
		# parameters and then inserts it into database if it is not present in DB.

		# Data structure of input parameters:-
		# enrollment --> string
		# name --> dictionary
		# dob --> dictionary
		# phone_numbers --> list of string
		# email --> list of string
		# father_name --> dictionary
		# year_of_join --> integer
		# year_of_pass --> integer
		# branch --> string
		# section --> string
		# gender --> string
		# temp_address --> string
		# perm_address --> string

		# Important Points:-
		# 1. enrollment is the primary key for the students Profile collection.
		# 2. collection name that is going to be used is : student_profile

		# Creating dictionary of the document that is going to insert in DB.
		document = {
				"enrollment": enrollment,
				"name": name,
				"phone_numbers": phone_numbers,
				"email": email,
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

		# Checking whether any student is already present in database with same enrollment
		duplicate_entry = db[config.Student_Profile_Collection].find_one({ f'enrollment':f'{enrollment}' })
		if duplicate_entry != None:
			print('[ Error ] Object of this Enrollment Number already present in Database')
			return False
		else:
			status = db[config.Student_Profile_Collection].insert_one(document)
			print(f'[ INFO  ] {status}') 	# Printing Status of result of query
			return True

		def remove(self,query_parameter,query_value):
			# This remove function inputs query parameter like enrollment, name, etc. and query value
			# to search documents in collection. After that remove them from collection
			status = db[config.Student_Profile_Collection].delete_many({ f'{query_parameter}':f'{query_value}' })
			print(f'[ INFO  ] {status}')

		#This update() function inputs the enrollment to check whether a student of this enrollment number
		# is present or not and then it updates the values
		def update(self,enrollment,updation_param,updation_value):
			searching_values = {'enrollment':f'{enrollment}'}
			updating_values = {f'{updation_param}':f'{updation_value}'}
			db[config.Student_Profile_Collection].update_one(searching_values, {'$set':updating_values})





## Start of Attendance Collection API
## --------------------------------------------------------------------------
## This attendance class is used for the following functions:-
## 1. Marking attendance with method name - mark
## 2. Show whole attendance collection with method name - show
## 3. Show attendance of any particular date with method name - show_on
## 4. Remove attendance collection with method name - remove
class attendance:
	def __init__(self,faculty_id,programme,branch,section,year_of_pass):
		# Constructor of attendance accepts the following parameters :
		# faculty_id --> Unique_ID of faculty --> string
		# programme --> Programme of class whose attendance needs to mark like BBA, BTech --> string
		# branch --> like CSE, IT, etc. --> string
		# section --> string
		# year_of_pass --> string

		# Creating a collection in database with identifier like 036_attendance_sheet_btech_a_2021
		# This collection object is gonna be used further for any operation like :-
		# Marking attendance, show, etc.
		self.collection = db[f'{faculty_id}_attendance_sheet_{programme}_{branch}_{section}_{year_of_pass}']

	def mark(self,attendance_dictionary):
		# Attendance_dictionary object contains a dictionary of that stores date on which attendance 
		# taken and the present status of students with their enrollment number
		# for example :
		# attendance_dictionary = {
		#						'date':	{ 'day':04,'month':06,'year':1998 },
		#						'attendance': {
		#								'03620802717':'P',         # Here P stands for Present
		#								'03720802717':'A',			# Here A stands for Absent
		#								'05520802717':'P'
		#							}
		#						}		
		status = self.collection.insert_one(attendance_dictionary)
		print(f'[ INFO  ] {status}') 	# Printing Status of result of query
		return True		

	def show(self):
		# This method doesn't inputs any parameter and returns the list of all the available
		# documents inside collection for which attendance constructor is initialised
		return list(self.collection.find({}))

	def show_on(self,query_date):
		# This method inputs date dictionary and returns list of attendance on that particular date
		return list(self.collection.find({ 'date': query_date }))





## Start of Feedback Collection API
## ----------------------------------------------------------------
## This feedback class is used for the following functions:-
## 1. Adding a feedback for a particular teacher with method name - add_message
## 2. Listing all the feedbacks with a teacher with method name -show_all
## 3. Removing a feedback for a teacher with method name - remove
class feedback:
    def __init__(self,enrollment,message,faculty_id):
        #Constructor of feedback accepts the following parameters:-
        # enrollment --> enrollment id of student --> string
        #message --> the feedback message --> string
        #faculty_id --> Unique_ID of faculty -->string

        #Creating a collection in database with identifier like 05520802717_message_036
        #This collection object is gonna be used further for any operation like:-
        #adding the feedback, show_all,etc.
        self.collection = db[f'{enrollment}_message_{faculty_id}']

    def add_message(self,feedback_dictionary):
        #feedback_dictionary contains a dictionary of that stores date on which the
        #feedback was given , the faculty_id of the teacher to wchich the feedback was
        #given and the message with the student's enrollment number.
        #for example:
        #feedback_dictionary = {
        #                       'date': {'day': 07,'month':11,'year':2000},
        #                       'faculty_id':faculty_id
        #                       'feedback': {
        #                                   '05520802717':'nice methods used by ma'am',
        #                                   '03720802717':'excellent'
        #                                   }
        #                       }
        status = self.collection.insert_one(feedback_dictionary)
        print (f'[INFO]{status}') #Printing status of result of query
        return True

    def show_all(self):
        #This method doesn't inputs any parameter and returns the list of all the
        #available documents inside collection for which the feedback constructor is initialized.
        return list(self.collection.find({}))




if __name__ == '__main__':
	# Enter testing code here
  pass
