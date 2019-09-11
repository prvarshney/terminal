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
		duplicate_entry = db.collection.find_one({ 'enrollment':feedback_dictionary[enrollment] })
		if duplicate_entry != None:
			print('[ ERROR ] Feedback of this student already present in database for this faculty')
		else:
			status = self.collection.insert_one(feedback_dictionary)
			print (f'[INFO]{status}') #Printing status of result of query

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
    
 
if __name__ == '__main__':
	if DEBUG_STATUS:
		# This code is used to perform some CRUD operations on API created above
		# You can comment this out if you wants to avoid its running
		# Enter testing code below END OF DEBUG CODE
		print('---------------------------------------------------------')
		print('[ INFO  ] Program running in Debug Mode')
		print('---------------------------------------------------------')
		print('\n[ INFO  ] Checking Faculty API')
		print('[ INFO  ] Inserting a Faculty Profile')
		faculty = faculty()
		faculty.insert(
			id='F364A',
			name={'f_name':'Deepali','m_name':'','l_name':'Virmani'},
			dob={ 'day':'04','month':'06','year':'1998' },
			phone_numbers=['011-27883979','7428306355'],
			email=['cse_hod@gmail.com'],
			subjects=['Networking','Machine Learning','Artificial Intelligence'],
			qualifications=['Btech CSE','Mtech CSE','Phd. AI'],
			time_table={
					'monday':['cse-a-2021','cse-b-2021','un-scheduled',
							'un-scheduled','cse-a-2021-lab','cse-a-2021',
							'un-scheduled'],
					'tuesday':['cse-a-2021','cse-b-2021','un-scheduled',
							'un-scheduled','cse-a-2021-lab','cse-a-2021',
							'un-scheduled'],
					'wednesday':['cse-a-2021','cse-b-2021','un-scheduled',
							'un-scheduled','cse-a-2021-lab','cse-a-2021',
							'un-scheduled'],
					'thursday':['cse-a-2021','cse-b-2021','un-scheduled',
							'un-scheduled','cse-a-2021-lab','cse-a-2021',
							'un-scheduled'],
					'friday':['cse-a-2021','cse-b-2021','un-scheduled',
							'un-scheduled','cse-a-2021-lab','cse-a-2021',
							'un-scheduled'],
					},
			classes=['cse-a-2012','cse-b-2021'],
			ratings='4.3'
			)
		# waiting for key dump to continue
		input(f'[ INFO  ] Check on MongoDB Server for any Insertion in {config.Faculty_Profile_Collection} Collection ')

		print(f'[ INFO  ] Querying  in {config.Faculty_Profile_Collection} Collection ')
		res = faculty.query('faculty_id','F364A')
		print('[ INFO  ] Received Documents : ')
		print(res)

		print('[ INFO  ] Checking Update Method')
		faculty.update('F364A','name',{'f_name':'Meenakshi','m_name':'','l_name':''})
		input(f'[ INFO  ] Check on MongoDB Server for any Updation in {config.Faculty_Profile_Collection} Collection ')

		print(f'[ INFO  ] Removing Inserted Document from {config.Faculty_Profile_Collection} Collection')
		faculty.remove('faculty_id','F364A')
		input(f'[ INFO  ] Check on MongoDB Server for any Deletion in {config.Faculty_Profile_Collection} Collection ')

		print('\n---------------------------------------------------------')
		print('[ INFO  ] Checking Student API')
		student = student()
		print('[ INFO  ] Inserting a Student Profile')
		student.insert(
			enrollment='03620802717',
			name={'f_name':'Prashant','m_name':'','l_name':'Varshney'},
			phone_numbers=['7428206355','7982068083'],
			email=['pv03158@gmail.com','varshney.prashant98@gmail.com'],
			father_name={'f_name':'Girish','m_name':'Chandra','l_name':'Varshney'},
			year_of_join='2017',
			year_of_pass='2021',
			programme='btech',
			branch='cse',
			section='a',
			gender='m',
			dob={ 'day':'04','month':'06','year':'1998' },
			temp_address='Samaypur, Delhi - 110042',
			perm_address='CD Block, Pitampura'
			)
		# waiting for key dump to continues
		input(f'[ INFO  ] Check on MongoDB Server for any Insertion in {config.Student_Profile_Collection} Collection ')

		print(f'[ INFO  ] Querying  in {config.Student_Profile_Collection} Collection ')
		res = student.query('enrollment','03620802717')
		print('[ INFO  ] Received Documents : ')
		print(res)

		print('[ INFO  ] Checking Update Method')
		student.update('03620802717','name',{'f_name':'Preeti','m_name':'','l_name':'Yadav'})
		input(f'[ INFO  ] Check on MongoDB Server for any Updation in {config.Student_Profile_Collection} Collection ')

		print(f'[ INFO  ] Removing Inserted Document from {config.Student_Profile_Collection} Collection')
		student.remove('enrollment','03620802717')
		input(f'[ INFO  ] Check on MongoDB Server for any Deletion in {config.Student_Profile_Collection} Collection ')

		print('\n---------------------------------------------------------')
		print('[ INFO  ] Checking Attendance API')
		attendance = attendance('F364A','btech','machine_learning','cse','a','5','2021')
		print('[ INFO  ] Inserting a Attendance Document')
		attendance.insert({
						'date':	{ 'day':'04','month':'06','year':'1998' },
						'attendance': {
								'03620802717':'P',
								'03720802717':'A',
								'05520802717':'P'
								}
						})
		input(f'[ INFO  ] Check on MongoDB Server for any Creation of Attendance Collection ')

		print(f'[ INFO  ] Querying  in Attendance Collection ')
		res = attendance.show()
		print('[ INFO  ] Received Documents : ')
		print(res)

		print(f'[ INFO  ] Querying  in Attendance Collection for date : 04-06-1998')
		res = attendance.show_on({ 'day':'04','month':'06','year':'1998' })
		print('[ INFO  ] Received Documents : ')
		print(res)

		print(f'[ INFO  ] Updation in Attendance Collection ')
		attendance.update(
						{ 'day':'04','month':'06','year':'1998' },
						{
						'date':	{ 'day':'04','month':'06','year':'1998' },
						'attendance': {
								'03620802717':'P',
								'03720802717':'P',
								'05520802717':'P'
									}
						})
		input(f'[ INFO  ] Check on MongoDB Server for any Updation in Attendance Collection ')
		print(f'[ INFO  ] Dropping Attendance Collection')
		attendance.remove()
		input(f'[ INFO  ] Check on MongoDB Server for any Deletion in Attendance Collection ')

		print('\n---------------------------------------------------------')
		print('[ INFO  ] Checking Marksheet API')
		marksheet = marksheet('F364A','btech','maths','cse','a','5','2021')
		print('[ INFO  ] Inserting a Marksheet Document')
		marksheet.insert({
						'enrollment':	'03720802717' ,
						'marks': '29',
						'assessment':'8'
						})
		input(f'[ INFO  ] Check on MongoDB Server for any Creation of Marksheet Collection ')

		print(f'[ INFO  ] Querying  in Marksheet Collection ')
		res = marksheet.show()
		print('[ INFO  ] Received Documents : ')
		print(res)

		print(f'[ INFO  ] Querying  in Marksheet Collection for enrollment: 03720802717')
		res = marksheet.show_on('03720802717')
		print('[ INFO  ] Received Documents : ')
		print(res)
		print(f'[ INFO  ] Updation in Marksheet Collection ')
		marksheet.update(
		 				 '03720802717',
		 				 {'enrollment':'03720802717',
						  'marks': '27',
						  'assessment':'8'
						  })
		input(f'[ INFO  ] Check on MongoDB Server for any Updation in Marksheet Collection ')
		print(f'[ INFO  ] Dropping Marksheet Collection')
		marksheet.remove('03720802717')
		input(f'[ INFO  ] Check on MongoDB Server for any Deletion in Marksheet Collection ')

  print('\n---------------------------------------------------------------------')
		print('[ INFO  ] Checking Feedback API')
		feedback = feedback('A401', 'COA', 'B.tech', 'CSE', 'A', '3', '2021')
		print('[ INFO  ] Inserting a feedback document')
		feedback.insert({
			'date': {'day': '04', 'month': '06', 'year': '1998'},
			'enrollment': '05520802717',
			'feedback': 'nice work'
		}, '05520802717')
		input(f'[ INFO  ] Check on MongoDB Server for any creation of Feedback Collection ')
	
		print(f'[ INFO  ] Querying in Feedback Collection')
		res = feedback.show_all()
		print('[ INFO  ] Recieved Documents : ')
		print(res)

		print('[ INFO  ] Updation in Feedback Collection. ')
		feedback.update('05520802717', { 
				'date': {'day': '04' , 'month':'06','year':'2000'},
				'enrollment':'05520802717',
				'feedback': 'lol'
		 		})

		input(f'[ INFO  ] Check on MongoDB Server for any Updation in Feedback Collection ')
		print('[ INFO  ] Deleting a particular feedback ')
		feedback.remove_particular('05520802717')
		print('[ INFO  ] Feedback deleted of this student.')

		print('[ INFO  ] Dropping the feedback_sheet for the particular faculty. ')
		feedback.remove_all()
		print('[ INFO  ] Check on Mongo DB Server for any deletion in Feedback Collection.')
	################################ END OF DEBUG CODE ########################################
