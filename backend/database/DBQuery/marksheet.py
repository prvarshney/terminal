from pymongo import MongoClient
import sys
import config
from logger import log

## Start of Marksheet Collection API
## --------------------------------------------------------------------------
## This marksheet class is used for the following functions:-
## 1. Uploading marks with method name - insert
## 2. Show whole marks collection with method name - show_all
## 3. Show marks of any particular student using their enrollment number with method name - show_of
## 4. Remove marks collection with method name - remove
## 5. Update marks of any particular student with method name - update
##
class Marksheet:
	def __init__(self, faculty_id, subject, programme, branch, section, year_of_pass, semester):
		# Constructor of marksheet accepts the following parameters:
		# faculty_id --> Unique Id of faculty --> string
		# subject --> subject name taught by the given faculty --> string
		# programme --> programme of the class whose marks are provided here --> string
		# branch --> like cse, IT etc --> string
		# section --> string
		# year_of_pass --> string
		# semester --> string
		#
		# Creating a collection in database with identifier like
		# "037_maths_btech_cse_a_2021_4".
		#
		try:
			self.client = MongoClient(config.MongoDB_URI)
			db = self.client[config.Marksheet_DB]
			log('[ INFO  ] Marksheet_DB Connected Successfully')
		except:
			log('[ Error ] Unable To Create Connection With Marksheet_DB')
			sys.exit(0)
		self.collection = db[f'{faculty_id}_{subject}_{programme}_{branch}_{section}_{year_of_pass}_{semester}']

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
			log('[ Error ] Object of this Enrollment Number already present in Database')
			return 417
		else:
			status = self.collection.insert_one(marksheet_dictionary)
			log(f'[ INFO  ] {status}') 	# Printing Status of result of query
			log('[ INFO  ] Marks of the enrollment number inserted in Marksheet_DB.')
			return 201

	def show_of(self,enrollment):
		# This method inputs enrollment and returns marks of that particular enrollment.
		# -------------------------------------------------------------------------------
		# Data Structures of input parameter :-
		# enrollment --> string
		#
		try:
			res = list(self.collection.find({ 'enrollment': enrollment }))
			log('[ INFO  ] Marks of the enrollment has been displayed.')
			response = {
				'status':'202',
				'res':res
			}
		except:
			response = {
				'status':'404',
				'res':'NA'
			}
		return response

	def show_all(self):
		# This method doesn't takes any input and returns marks of all students.
		# -------------------------------------------------------------------------------
		#
		try:
			res =  list(self.collection.find({}))
			log('[ INFO  ] Marks of all the students has been successfully displayed.')
			response = {
				'status':'302',
				'res':res
			}
		except:
			response = {
				'status':'598',
				'res':'NA'
			}
		return response

	def remove(self,enrollment):
		# This method removes the collection of marks of a particular
		# enrollment from the class.
		# ----------------------------------------------------------------------------------
		# Data Structures of input parameter :-
		# enrollment --> string
		#
		try:
			status = self.collection.delete_many({ 'enrollment':enrollment })
			log(f'[ INFO  ] {status}') 	# Printing Status of result of query
			log('[ INFO  ] Marks of particular enrollment has been removed.')
			return 220
		except:
			return 203

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
		try:
			status = self.collection.update_many( searching_values, {'$set':updation_value} )
			log(f'[ INFO  ] {status}') 	# Printing Status of result of query
			log('[ INFO  ] Marksheet_DB has been updated.')
			return 301
		except:
			return 204


	def __del__(self):
		self.client.close()

if __name__ == "__main__":
	# TEST CODE COMES HERE
	pass
