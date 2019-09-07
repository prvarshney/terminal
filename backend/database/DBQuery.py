# This module acts as an API for CRUD operations in database
from pymongo import MongoClient
import config

# Creating connection with the mongodb database
client = MongoClient(config.MongoDB_URI)        # Use this client object to query database
db = client[config.Database_Name]               # Use this db object to query collections


## This faculty class used for the following functions :
## 1. Inserting faculty profile with method name - insert
## 2. Deleting faculty profile with method name - remove
## 3. Querying faculty profile with method name - query
## 4. Update faculty profile with method name - update

class faculty:
	def insert(self,id,name,phone_numbers,email,subjects,qualifications=[],time_table={},classes=[],ratings=5,reviews=[]):
		# This insert method inputs necessary details of faculty through input parameters and then
	    # insert it into database if it doesn't presents in DB
	    #
	    # Datastructure of input parameters :
	    # id --> integer
	    # name --> string
	    # phone numbers --> list of integer value
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
			    "phone_numbers":phone_numbers,
			    "email":email,
			    "subjects":subjects,
			    "qualifications":qualifications,
			    "time-table":time_table,
			    "classes":classes,
			    "ratings":ratings,
			    "reviews":reviews
	    		}
	    status = db.faculty_profile.insert_one(document)
	################### End of insert method ####################
	

