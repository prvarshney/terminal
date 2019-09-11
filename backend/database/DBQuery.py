## This module acts as an API for CRUD operations in database
## Note for any CRUD operation on database always use lowercase alphabets
##
from pymongo import MongoClient
import config
import sys


# Global variables
DEBUG_STATUS = True	# Change this Debug Status to True for debugging and checking APIs

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
##
class faculty:
	def insert(self,id,name,dob,phone_numbers,email,subjects,qualifications=[],
		time_table={},classes=[],ratings=5):
		# This insert method inputs necessary details of faculty through
		# input parameters and then insert it into database if it doesn't presents in DB
		#--------------------------------------------------------------------------------
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
		# ratings --> string
		#
		# Important Points :
		# 	*qualifications, time-table, classes, ratings, reviews are optional parameters if not
		# 	 provided default values are used
		# 	*id is the primary key for faculty profile collections
		# 	*collection name that is going to be used : faculty_profile
		#
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
	    		}

	    # Checking whether any faculty with same faculty_id is present in database
	    duplicate_entry = db[config.Faculty_Profile_Collection].find_one({ 'faculty_id':id })
	    if duplicate_entry != None:		# Run when their presents any duplicate faculty_id in db
	    	print('[ Error ] Object of this ID already present in database')
	    	return False
	    else:			# Runs when there doesn't present any duplicate entry
		    status = db[config.Faculty_Profile_Collection].insert_one(document)
		    print(f'[ INFO  ] {status}') 	# Printing Status of result of query
		    return True


	def query(self,query_parameter,query_value):
		# This query function inputs query parameter like faculty_id, name, etc. and query value
		# to search documents in collection. After successful search it returns
		# rest of the details to the user.
		# -----------------------------------------------------------------------
		# Data Structure of input parameters :-
		# query_parameter --> string
		# query_value --> string, dictionary, list
		#
		return list(db[config.Faculty_Profile_Collection].find_({ query_parameter:query_value }))


	def remove(self,query_parameter,query_value):
		# This remove function deletes those documents from collection which have query_parameter
		# as a key and query_value as a value
		#----------------------------------------------------------------------------------
		# Data Structures of input parameters :
		# query_parameter --> string
		# query_value --> string,dictionary or list
		#
		status = db[config.Faculty_Profile_Collection].delete_many({ query_parameter:query_value })
		print(f'[ INFO  ] {status}')


	def update(self,faculty_id,updation_param,updation_value):
		# This update function inputs the faculty_id to check which document needs to update
		# and then updates the updation_param with updation_value
		# ----------------------------------------------------------------------------------
		# Data Structures of input parameters :
		# faculty_id --> string
		# updation_param --> string
		# updation value --> for id,ratings as updation_param --> string
		#				 --> for name,dob,timetable --> dictionary
		#				 --> for phone_numbers, email, subject, qualification, classes --> list of string
		#
		searching_values = {'faculty_id':faculty_id }
		updating_values = { updation_param:updation_value }
		status = db[config.Faculty_Profile_Collection].update_one(searching_values, {'$set':updating_values})
		print(f'[ INFO  ] {status}')


## Start of Student's Profile Collection API
## --------------------------------------------------------------------------
## This student profile class is used for the following functions:-
## 1. Inserting student profile with method name - insert
## 2. Deleting student profile with method name - delete
## 3. Querying student profile with method name - query
## 4. Update student profile with method name - update
##
class student:
	def insert(self, enrollment, name, phone_numbers, email, father_name, year_of_join,year_of_pass,
	 programme,branch, section, gender, dob, temp_address, perm_address):
		# This insert method inputs necessary details of student through input
		# parameters and then inserts it into database if it is not present in DB.
		#
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
		#
		# Important Points:-
		# 1. enrollment is the primary key for the students Profile collection.
		# 2. collection name that is going to be used is : student_profile
		#
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
		#
		# Checking whether any student is already present in database with same enrollment
		duplicate_entry = db[config.Student_Profile_Collection].find_one({ enrollment:enrollment })
		if duplicate_entry != None:
			print('[ Error ] Object of this Enrollment Number already present in Database')
			return False
		else:
			status = db[config.Student_Profile_Collection].insert_one(document)
			print(f'[ INFO  ] {status}') 	# Printing Status of result of query
			return True


	def query(self,query_parameter,query_value):
		# This query function inputs query parameter like enrollment_id, name, etc. and query value
		# to search documents in collection. After successful search it returns
		# rest of the details to the user.
		# ---------------------------------------------------------------------------------
		# Data Structures of input parameters :-
		# query_parameter --> string
		# query_value --> string, dictionary, list of string
		#
		return list(db[config.Student_Profile_Collection].find({ query_parameter:query_value }))


	def remove(self,query_parameter,query_value):
		# This function removes those documents which possess query_parameter as any key
		# and query_value as their values from collection
		#------------------------------------------------------------------------------------
		# Data Structures of input parameters :-
		# query_parameter --> string
		# query_value --> list, string, dictionary
		#
		status = db[config.Student_Profile_Collection].delete_many({ query_parameter:query_value })
		print(f'[ INFO  ] {status}')


	def update(self,enrollment,updation_param,updation_value):
		# This update function inputs the enrollment, to check which document needs to update
		# and then, updates the updation_param with updation_value.
		# --------------------------------------------------------------------------------------
		# Data Structures of input parameters :-
		# enrollment --> string
		# updation_param --> string
		# updation_value --> string, list, dictionary
		#
		searching_values = {'enrollment':enrollment}
		updating_values = { updation_param:updation_value }
		status = db[config.Student_Profile_Collection].update_one(searching_values, {'$set':updating_values})
		print(f'[ INFO  ] {status}')


## Start of Attendance Collection API
## --------------------------------------------------------------------------
## This attendance class is used for the following functions:-
## 1. Marking attendance with method name - insert
## 2. Show whole attendance collection with method name - show_all
## 3. Show attendance of any particular date with method name - show_on
## 4. Remove attendance collection with method name - remove
## 5. Update attendance of any particular date with method name - update
class attendance:
	def __init__(self,faculty_id,programme,subject,branch,section,semester,year_of_pass):
		# Constructor of attendance accepts the following parameters :
		# faculty_id --> Unique_ID of faculty --> string
		# programme --> Programme of class whose attendance needs to mark like BBA, BTech --> string
		# subject --> String
		# branch --> like cse, ece, etc. --> string
		# section --> string
		# semester --> string
		# year_of_pass --> string
		#
		# Creating a collection in database with identifier like
		# F45A_btech_java_cse_a_5_2021
		# This collection object is gonna be used further for any operation like :-
		# Marking attendance, show, etc.
		#
		self.collection = db[f'{faculty_id}_attendance_sheet_{programme}_{subject}_{branch}_{section}_{semester}_{year_of_pass}']


	def insert(self,attendance_dictionary):
		# Attendance_dictionary object contains a dictionary, that stores date on which attendance
		# taken and the present status of students with their enrollment number
		# ------------------------------------------------------------------------------------
		# for example :
		# attendance_dictionary = {
		#						'date':	{ 'day':04,'month':06,'year':1998 },
		#						'attendance': {
		#								'03620802717':'P',         # Here P stands for Present
		#								'03720802717':'A',			# Here A stands for Absent
		#								'05520802717':'P'
		#							}
		#						}
		#
		status = self.collection.insert_one(attendance_dictionary)
		print(f'[ INFO  ] {status}') 	# Printing Status of result of query
		return True


	def show_all(self):
		# This method doesn't inputs any parameter and returns the list of all the available
		# documents inside collection for which attendance constructor is initialised
		#
		return list(self.collection.find({}))


	def show_on(self,query_date):
		# This method inputs date dictionary and returns list of attendance on that
		# particular date
		# ------------------------------------------------------------------------------------
		# Data Structures of input parameter :-
		# query_date --> dictionary
		#
		return list(self.collection.find({ 'date': query_date }))


	def remove(self):
		# This method removes the collection of attendance of that particular faculty_id for
		# which class object is intialised.
		#
		self.collection.drop()


	def update(self,date,attendance_dictionary):
		# This method use to update attendance of a particular date with attendance_dictionary
		# object
		# ----------------------------------------------------------------------------------
		# Data Structures of input parameters :-
		# date --> dictionary
		# attendance_dictionary --> dictionary
		#
		searching_values = { 'date':date }
		updation_value = attendance_dictionary
		status = self.collection.update_many(searching_values, {'$set':updation_value})



## Start of Marksheet Collection API
## --------------------------------------------------------------------------
## This marksheet class is used for the following functions:-
## 1. Uploading marks with method name - insert
## 2. Show whole marks collection with method name - show_all
## 3. Show marks of any particular student using their enrollment number with method name - show_of
## 4. Remove marks collection with method name - remove
## 5. Update marks of any particular student with method name - update
##
class marksheet:
	def __init__(self, faculty_id, programme, subject, branch, section, semester, year_of_pass):
		# Constructor of marksheet accepts the following parameters:
		# faculty_id --> Unique Id of faculty --> string
		# programme --> programme of the class whose marks are provided here --> string
		# subject --> subject name taught by the given faculty --> string
		# branch --> like cse, IT etc --> string
		# section --> string
		# semester --> string
		# year_of_pass --> string
		#
		# Creating a collection in database with identifier like
		# "037_marksheet_btech_maths_cse_a_4_2021".
		#
		self.collection = db[f'{faculty_id}_marksheet_{programme}_{subject}_{branch}_{section}_{semester}_{year_of_pass}']


	def insert(self,marksheet_dictionary):
		# inserts marksheet dictionary that contains enrollment, marks and assessment
		# if it already isn't available in db.
		# -----------------------------------------------------------------------------------
		# for example :
		# marksheet_dictionary = {
		#							'enrollment':'03720802717',
		#							'marks' :  '29',
		#							'assessment':'8'
		#						}
		#
		duplicate_entry = self.collection.find_one({
				'enrollment':marksheet_dictionary['enrollment']
				})
		if duplicate_entry != None:
			print('[ Error ] Object of this Enrollment Number already present in Database')
			return False
		else:
			status = self.collection.insert_one(marksheet_dictionary)
			print(f'[ INFO  ] {status}') 	# Printing Status of result of query
			return True


	def show_of(self,enrollment):
		# This method inputs enrollment and returns marks of that particular enrollment.
		# -------------------------------------------------------------------------------
		# Data Structures of input parameter :-
		# enrollment --> string
		#
		return self.collection.find({ 'enrollment': enrollment })

	def show_all(self):
		# This method doesn't takes any input and returns marks of all students.
		# -------------------------------------------------------------------------------
		#
		return list(self.collection.find({}))


	def remove(self,enrollment):
		# This method removes the collection of marks of a particular
		# enrollment from the class.
		# ----------------------------------------------------------------------------------
		# Data Structures of input parameter :-
		# enrollment --> string
		#
		status = self.collection.delete_many({ 'enrollment':enrollment })
		print(f'[ INFO  ] {status}') 	# Printing Status of result of query


	def update(self,enrollment,marksheet_dictionary):
		# This method use to update marks of a particular enrollment
		# with marksheet_dictionary object
		# --------------------------------------------------------------------------------
		# Data Structures of the input parameters :-
		# enrollment --> string
		# marksheet_dictionary --> dictionary
		#
		searching_values = { 'enrollment':enrollment }
		updation_value = marksheet_dictionary
		status = self.collection.update_many( searching_values, {'$set':updation_value} )
		print(f'[ INFO  ] {status}') 	# Printing Status of result of query



## Start of studymaterial Collection API
## --------------------------------------------------------------------------
## This class is used for the following functions:-
## 1. Insert Notes/Assignment with method name - insert
## 2. Show whole Notes/Assignment collection with method name - show_all
## 3. Remove whole studymaterial collection with method name - remove_all
## 5. Remove a particular Notes/Assignment of any particular title with method name - remove
class studymaterial:
	def __init__(self,faculty_id,programme,subject,branch,section,semester,year_of_pass):
		# Constructor of studymaterial accepts the following parameters :
		# faculty_id --> Unique_ID of faculty --> string
		# programme --> Programme of class whose attendance needs to mark like BBA, BTech --> string
		# subject --> String
		# branch --> like CSE, IT, etc. --> string
		# section --> string
		# semester --> string
		# year_of_pass --> string
		#
		# Creating a collection in database with identifier like 036_study_material_btech_java_a_5_2021
		# This collection object is gonna be used further for any operation like :-
		# Inserting notes, show_all, etc.
		#
		self.collection = db[f'{faculty_id}_study_material_{programme}_{subject}_{branch}_{section}_{semester}_{year_of_pass}']


	def insert(self,title,date,path):
		# This method is used to insert absolute path of notes/assignment document
		# in the server.
		# -------------------------------------------------------------------------
		# DataStructures of the input parameters are :
		# title --> stores the title of the note --> string
		# date --> stores the date on which note is stored on database --> dictionary
		# path --> path of the note/assignment file stored in database --> string
		#
		# here primary key is path of the notes/assignment
		duplicate_entry = self.collection.find_one({ 'path':path })		# checks whether the path of notes is already in db
		if duplicate_entry != None:
			print('[ Error ] Object of this title already present in Database')
			return False
		else:
			self.collection.insert_one({
				'date': date,
				'title':title,
				'path':path
				})
			return True


	def show_all(self):
		# This method used to fetch whole collection of studymaterial
		# It doesn't inputs any parameter and returns a list of dictionaries
		#
		return list(self.collection.find({}))


	def remove(self,title):
		# This method used to remove a document from study_material collection of the
		# basis of title.
		# -------------------------------------------------------------------------------
		# Data Structure of input parameter :
		# title --> string
		#
		status = self.collection.delete_many({ 'title':title })
		print(f'[ INFO  ] {status}')

	def remove_all(self):
		# This Method removes whole collection of that faculty studymaterial collection
		# for which its object is initialised.
		#
		status = self.collection.drop()


## Start of Feedback Collection API
## ------------------------------------------------------------------------------------------
## This feedback class is used for the following functions:-
## 1. Adding a feedback for a particular teacher with method name - insert
## 2. Listing all the feedbacks of a teacher with method name - show_all
## 3. Removing all the feedback of a teacher with method name - remove_all
## 4. Remove feedback by a particular studene with method name - remove
##
class feedback:
	def __init__(self,faculty_id,programme,subject,branch,section,semester,year_of_pass):
		# Constructor of feedback accepts the following parameters:-
		# faculty_id --> Unique_ID of faculty --> string
		# subject --> mathematics, coa, etc. --> string
		# programme --> e.g. btech, bba, etc. --> string
		# branch --> like cse, ece, etc. --> string
		# section --> string
		# semester --> string
		# year_of_pass --> string
		#
		# Creating a collection in database with identifier like :-
		# "f034a_feedback_sheet_btech_coa_cse_a_4_2021"
		#
		# This collection object is gonna be used further for any operation like:-
		# adding the feedback, show_all,etc.
		self.collection = db[f'{faculty_id}_feedback_sheet_{programme}_{subject}_{branch}_{section}_{semester}_{year_of_pass}']

	def insert(self,feedback_dictionary):
		# This method is used to add a feedback of any faculty by a particular class.
		# feedback_dictionary is a dictionary, that stores date on which the
		# feedback was given, enrollment of student that gives feedback,
		# and the feedback.
		# for example:
		# feedback_dictionary = {
		#                       'date': { 'day': '07','month':'11','year':'2000' },
		#                       'enrollment': '03620802717',
		#                       'feedback': 'best teacher'
		#                       }
		#
		duplicate_entry = self.collection.find_one({ 'enrollment':feedback_dictionary['enrollment'] })
		if duplicate_entry != None:
			print('[ ERROR ] Feedback of this student already present in database for this faculty')
		else:
			status = self.collection.insert_one(feedback_dictionary)
			print (f'[ INFO  ]{status}') #Printing status of result of query

	def show_all(self):
		# This method doesn't inputs any parameter and returns a list of all the
		# available documents inside collection for which the feedback constructor is initialized.
		# This method displays all the feedbacks of a particular faculty given by a particular class
		# student
		#
		return list(self.collection.find({}))

	def remove_all(self):
		# This method removes the collection of feedback of that particular faculty_id for
		# which class object is initialized.
		# For example:- if any teacher has left, then all the feedbacks of that particular
		# faculty must be deleted.
		#
		self.collection.drop()


	def remove(self,enrollment):
		# This method is used to remove the feedback by a student for a particular faculty.
		#
		status = self.collection.delete_one({ 'enrollment':enrollment })
		print(f'[ INFO  ] {status}')


	def update(self,feedback_dictionary):
		# This update method inputs the feedback_dictionary to check which document needs
		# to be updated and then, updates it.
		#
		searching_values = { 'enrollment':feedback_dictionary['enrollment'] }
		updating_values = feedback_dictionary
		status = self.collection.update_one(searching_values, {'$set':updating_values})

##Start of previous_class_sheet API
##----------------------------------------------------------------------
##This previous_class_sheet stores the different subjects that the faculty
##had taught in the previous semesters
##This previous_class_sheet is used for the following functions:
##1.Inserting different classes with their subjects  using the method name - insert
##2.Updating the subject name or the class name using the method name - update
##3.Removing a particular class or subject with method name - remove
##4.Removing all the classes or the subjects for the faculty with method name - remove_all
##5.To display all the subjects taught by a faculty for the classes with method name - show_all
##
class previous_class_sheet:
	def __init__(self, faculty_id):
        #Constructor of previous_class_sheet accepts the following parameters:
        #faculty_id --> unique ID for the faculty --> string
        #
        #Creating a collection in database with identifier like :-
        #037_previous_classes
        # This collection object is gonna be used for further operation like-
		# Inserting, updating or removing the subjects from the faculty list.
		#
        self.collection = db[f'{faculty_id}_previous_classes']

    def insert(self,subject,semester,programme,branch,section,year_of_pass):
        # previous_classes_dictionary object contains a dictionary that stores the previous
		# subject with the previous semester and the previous class name and batch.
        #------------------------------------------------------------------------------------
        #Data structure of input parameters :-
        # subject --> string
		# semester --> string
		# programme --> string
		# branch --> string
		# section --> string
		# year_of_pass --> string
		#
		# Creating dictionary of the document that is to be inserted in DB.
		#
		previous_classes_dictionary = {
			"subject" : subject,
			"semster" : semester,
			"previous_batch" : f'batch_{programme}_{branch}_{section}_{year_of_pass}'
		}
		duplicate_entry = self.collection.find_one({'previous_batch':previous_classes_dictionary['previous_batch']})
		if duplicate_entry != None:
			print('[ ERROR ] This subject and class is already present in database '
				  'for this faculty')
		else:
			status = self.collection.insert_one(previous_classes_dictionary)
			print (f'[INFO]{status}') #Printing status of result of query

    def update(self,programme,branch,section,year_of_pass,new_semester,new_subject,
    new_programme,new_branch,new_section,new_year_of_pass):
        # This method is used to update the classes or subjects of a faculty.
		# ------------------------------------------------------------------
		# Data Structure of input parameters:-
		# programme --> string
		# branch --> string
		# section --> string
		# year_of_pass --> string
		# new_subject --> string
		# new_semester --> string
		# new_programme --> string
		# new_branch --> string
		# new_section --> string
		# new_year_of_pass --> string
		#
		# Creating previous_batch -
		#
        previous_batch = f'batch_{programme}_{branch}_{section}_{year_of_pass}'
		# Creating dictionary of the updated previous_class:-
		#
		previous_classes_dictionary = {
			"subject" : new_subject,
			"semester" : new_semester,
			"previous_batch" : f'batch_{new_programme}_{new_branch}_{new_section}_'
			f'{new_year_of_pass}'
		}
		searching_values = {'previous_batch': previous_batch}
		updation_value = previous_classes_dictionary
		status = self.collection.update_one(searching_values, {'$set':updation_value})

    def remove(self,programme,branch,section,year_of_pass):
		# This method removes the record of that class from the faculty
		# previous class list.
		# ----------------------------------------------------------------------
		# Data Structure of input parameter:-
		# previous_batch --> string
		#
		status = self.collection.delete_many({'previous_batch':f'batch_{programme}_'
		f'{branch}_{section}_{year_of_pass}'})
		print(f'[ INFO  ]{status}')      #Printing status of result of query

    def remove_all(self):
		# This method removes all the subjects and classes of the faculty.
		#  e.g. Suppose a faculty leaves the college
		#  so there is no need to maintain the previous class sheet for that
		#  faculty.
		#
		self.collection.drop()

    def show_all(self):
		# This method doesn't take any input parameter.
		# It returns the list of all the available documents inside
		# collection for which the previous_classes constructor has been
		#  initialized.
		#
		return list(self.collection.find({}))



## Start of current_classes_sheet API
## ------------------------------------------------------
## This current_classes_sheet API is used to store the different subjects that a faculty
## takes for different classes.
## This current_classes_sheet is used for the following functions:-
## 1. Inseting the different classes with their subjects with method name - insert
## 2. Updating or editing the class name or the subject name with method name - update
## 3. Removing the particular class or subject with method name - remove
## 4. Removing all the classes or subjects for the faculty with method name - remove_all
## 5. To display all the subjects taught by a faculty for the classes with method name
##  - show_all
##
class current_classes_sheet:
	def __init__(self,faculty_id):
		# Constructor of current_classes_sheet accept the following parameters:
		# faculty_id --> Unique ID of faculty --> string
		#
		# Creating a collection in database with identifier like :-
		# 036_current_classes
		# This collection object is gonna be used for further operation like-
		# Inserting, updating or removing the subjects from the faculty list.
		#
		self.collection = db[f'{faculty_id}_current_classes']

	def insert(self,subject,semester,programme,branch,section,year_of_pass):
		# current_classes_dictionary object contains a dictionary that stores the present
		# subject with the current semester and the current class name and batch.
		# ----------------------------------------------------------------------
		# Data Structure of input parameters:-
		# subject --> string
		# semester --> string
		# programme --> string
		# branch --> string
		# section --> string
		# year_of_pass --> string
		#
		# Creating dictionary of the document that is to be inserted in DB.
		#
		current_classes_dictionary = {
			"subject" : subject,
			"semster" : semester,
			"current_batch" : f'batch_{programme}_{branch}_{section}_{year_of_pass}'
		}
		duplicate_entry = self.collection.find_one({'current_batch':current_classes_dictionary
		['current_batch']})
		if duplicate_entry != None:
			print('[ ERROR ] This subject and class is already present in database '
				  'for this faculty')
		else:
			status = self.collection.insert_one(current_classes_dictionary)
			print (f'[INFO]{status}') #Printing status of result of query

	def update(self,programme,branch,section,year_of_pass,new_subject,new_semester,
	new_programme,new_branch,new_section,new_year_of_pass):
		# This method is used to update the classes or subjects of a faculty.
		# ------------------------------------------------------------------
		# Data Structure of input parameters:-
		# programme --> string
		# branch --> string
		# section --> string
		# year_of_pass --> string
		# new_subject --> string
		# new_semester --> string
		# new_programme --> string
		# new_branch --> string
		# new_section --> string
		# new_year_of_pass --> string
		#
		# Creating current_batch -
		#
		current_batch = f'batch_{programme}_{branch}_{section}_{year_of_pass}'
		# Creating dictionary of the updated current_class:-
		#
		current_classes_dictionary = {
			"subject" : new_subject,
			"semester" : new_semester,
			"current_batch" : f'batch_{new_programme}_{new_branch}_{new_section}_'
			f'{new_year_of_pass}'
		}
		searching_values = {'current_batch': current_batch}
		updation_value = current_classes_dictionary
		status = self.collection.update_one(searching_values, {'$set':updation_value})

	def remove(self,programme,branch,section,year_of_pass):
		# This method removes the record of that class from the faculty
		# current class list.
		# --------------------------------------------------------------
		# Data Structure of input parameter:-
		# current_batch --> string
		#
		status = self.collection.delete_many({'current_batch':f'batch_{programme}_'
		f'{branch}_{section}_{year_of_pass}'})
		print(f'[ INFO  ]{status}')      #Printing status of result of query

	def remove_all(self):
		# This method removes all the subjects and classes of the faculty.
		#  e.g. Suppose a faculty leaves the college
		#  so there is no need to maintain the current class sheet for that
		#  faculty.
		#
		self.collection.drop()

	def show_all(self):
		# This method doesn't take any input parameter.
		# It returns the list of all the available documents inside
		# collection for which the current_classes constructor has been
		#  initialized.
		#
		return list(self.collection.find({}))

## Start of Batch Collection API
## ------------------------------------------------------------------------------------------
## This Batch class is used for the following functions:-
## 1. Adding a new batch with method name - insert
## 2. Listing all the students enrolled in a batch with method name - show_all
## 3. Removing all the enrolled students from batch with method name - remove_all
## 4. Remove any single student enrolled with method name - remove
##
class batch:
	def __init__(self,programme,branch,section,year_of_pass):
		# This constructor is used to create a required collection
		# in database. For Example :- batch_btech_cse_a_2021
		#
		self.collection = db[ f'batch_{programme}_{branch}_{section}_{year_of_pass}' ]


	def insert(self,enrollment):
		# Used to insert enrollment of a student in the required collection
		# ---------------------------------------------------------------------------
		# Data Structures of enrolled_students :-
		# enrollment --> string
		#
		# Checking for any duplicate entry in the collection
		duplicate_entry = self.collection.find_one({ 'enrollment':enrollment })
		print(duplicate_entry)
		if duplicate_entry != None:
			print('[ ERROR ] This Student Already Present in Database')
			return False
		else:
			status = self.collection.insert_one({ 'enrollment':enrollment })
			print(f'[ INFO  ] {status}')
			return False

	def remove(self,enrollment):
		# Used to remove enrollment of a particular student from batch collection
		# ----------------------------------------------------------------------------
		# Data Structures of input parameter :-
		# enrollment --> string
		#
		status = self.collection.delete_one({ 'enrollment':enrollment })
		print(f'[ INFO  ] {status}')


	def remove_all(self):
		# Used to remove whole collection for which batch class
		# Object is initialised.
		# ----------------------------------------------------------------------------
		#
		status = self.collection.drop()
		print(f'[ INFO  ] {status}')

	def show_all(self):
		# Used to display a list of all the enrolled students in a class
		return list(self.collection.find({}))

if __name__ == '__main__':
	# studymaterial = studymaterial(
	# 						faculty_id='F1U5K',
	# 						programme='btech',
	# 						subject='java',
	# 						branch='cse',
	# 						section='a',
	# 						semester='5',
	# 						year_of_pass='2021'
	# 						)
	# studymaterial.insert(
	# 					title='chapter_3_notes',
	# 					date={'day':'04','month':'06','year':'1998'},
  #
	# 					)
  #
  # print('--------------------------------------------------------------')
  # print('[ INFO  ] Checking current_classes_sheet API')
  # current_classes_sheet = current_classes_sheet('A016')
  # print(' [INFO  ] Inserting a current_classes document.')
  # current_classes_sheet.insert('toc','4','btech','cse','a','2021')
  # input(f'[ INFO  ] Check on MongoDB Server for any creation of Current class'
  #     f' Collection.')
  #
  # print(f'[ INFO  ] Querying in Current Class Collection.')
  # res = current_classes_sheet.show_all()
  # print('[ INFO  ] Recieved documents..')
  # print(res)
  #
  # print('[ INFO  ] Updation in Current Classes Collection..')
  # current_classes_sheet.update('btech','cse','a','2021','ds','3','btech','ece','a','2022')
  #
  # input(f'[ INFO  ] Check on Mongo DB Server for any Updation in current_classes_sheet'
  #     f' Collection.')
  # print('[ INFO  ] Deleting a particular class.')
  # current_classes_sheet.remove('btech','ece','a','2021')
  # print('[ INFO  ] Current class deleted from the sheet.')
  #
  # print('[ INFO  ] Dropping the current_classes_sheet for the particular faculty.')
  # current_classes_sheet.remove_all()
  # print('[ INFO  ] Check on Mongo DB Server for any deletion in current_classes_sheet'
  #     ' Collection.')

	previous_class_sheet.insert('maths','2','btech','cse','a','2021')
	input(f'[ INFO  ] Check on MongoDB Server for any creation of Current class'
    	f' Collection.')
################################ END OF DEBUG CODE ########################################
