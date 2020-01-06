from pymongo import MongoClient
import sys
import config
from logger import log

## START OF CURRENT_BATCHES API
## ------------------------------------------------------
## THIS CURRENT_BATCHES API IS USED TO APPLY CRUD OPERATIONS ON THE BATCHES ANY FACULTY
## IS CURRENTLY TAKING UNDER HIM/HER.
##
## THIS API IS USED FOR THE FOLLOWING FUNCTIONS:-
## 1. INSERTING DIFFERENT BATCHES THAT FACULTY IS TAKINGWITH METHOD NAME - INSERT
## 2. REMOVING THE PARTICULAR BATCH WITH METHOD NAME - REMOVE
## 3. REMOVING ALL THE BATCH FOR THE FACULTY WITH METHOD NAME - REMOVE_ALL
## 4. TO DISPLAY ALL THE BATCHES UNDER ANY FACULTY WITH METHOD NAME - SHOW_ALL
##
class CurrentBatches:
	def __init__(self,faculty_id):
		# CONSTRUCTOR OF CURRENT_BATCHES ACCEPT THE FOLLOWING PARAMETERS:
		# FACULTY_ID --> UNIQUE ID OF FACULTY --> STRING
		#
		# CREATING A COLLECTION IN DATABASE WITH IDENTIFIER LIKE :-
		# 036_CURRENT_BATCHES
		# THIS COLLECTION OBJECT IS GONNA BE USED FOR FURTHER OPERATION LIKE-
		# INSERTING, UPDATING OR REMOVING THE SUBJECTS FROM THE FACULTY LIST.
		#
		try:
			self.client = MongoClient(config.MongoDB_URI)
			self.faculty_id = faculty_id
			db = self.client[config.Current_Batches_DB]
			log(f'[  INFO  ] {config.Current_Batches_DB} Connected Successfully')
		except:
			log(f'[  ERROR ] Unable To Create Connection With {config.Current_Batches_DB}')
		self.collection = db[faculty_id]

	def insert(self,subject,semester,programme,branch,section,year_of_pass):
		# CURRENT_BATCHES_DICTIONARY OBJECT CONTAINS A DICTIONARY THAT STORES THE PRESENT
		# SUBJECT WITH THE CURRENT SEMESTER AND THE CURRENT CLASS NAME AND BATCH.
		# ----------------------------------------------------------------------
		# DATA STRUCTURE OF INPUT PARAMETERS:-
		# SUBJECT --> STRING
		# SEMESTER --> STRING
		# PROGRAMME --> STRING
		# BRANCH --> STRING
		# SECTION --> STRING
		# YEAR_OF_PASS --> STRING
		#
		# CREATING DICTIONARY OF THE DOCUMENT THAT IS TO BE INSERTED IN DB.
		current_batch_dictionary = {
			"subject" : subject,
			"semster" : semester,
			"batch" : f'{programme}_{branch}_{section}_{year_of_pass}'
		}
		try:
			duplicate_entry = self.collection.find_one(current_batch_dictionary)
			if duplicate_entry != None:
				log(f'[  ERROR ] Batch - {current_batch_dictionary} Is Already Present at Collection - {self.faculty_id} in Database - {config.Current_Batches_DB}')
				return 417
			else:
				status = self.collection.insert_one(current_batch_dictionary)
				log(f'[  INFO  ] {status}') #PRINTING STATUS OF RESULT OF QUERY
				log(f'[  INFO  ] Batch - {current_batch_dictionary} inserted at Collection - {self.faculty_id} in Database - {config.Current_Batches_DB}')
				return 201
		except:
			return 417
			log(f'[  ERROR ] API Failed to insert Batch - {current_batch_dictionary} at Collection - {self.faculty_id} in Database - {config.Current_Batches_DB}')

	def remove(self,subject,semester,programme,branch,section,year_of_pass):
		# THIS METHOD REMOVES THE RECORD OF THAT CLASS FROM THE FACULTY
		# CURRENT CLASS LIST.
		# --------------------------------------------------------------
		# DATA STRUCTURE OF INPUT PARAMETER:-
		# CURRENT_BATCH --> STRING
		#
		batch_dictionary = {
			"subject" : subject,
			"semster" : semester,
			"batch" : f'{programme}_{branch}_{section}_{year_of_pass}'
		}
		try:
			status = self.collection.delete_one( batch_dictionary )
			log(f'[  INFO  ] {status}')
			log(f'[  INFO  ] Batch - {batch_dictionary} has been removed successfully from Collection - {self.faculty_id} in Database - {config.Current_Batches_DB}')
			return 220
		except:
			log(f'[  ERROR ] API Failed to remove Batch - {batch_dictionary} from Collection - {self.faculty_id} in Database - {config.Current_Batches_DB}')
			return 203

	def remove_all(self):
		# THIS METHOD REMOVES ALL THE BATCHES ANY FACULTY IS CURRENTLY TAKING.
		# FOR EXAMPLE : SUPPOSE ANY FACULTY LEAVES THE COLLEGE
		# 				SO THERE IS NO NEED TO MAINTAIN THE CURRENT CLASS
		# 				SHEET FOR THAT FACULTY.
		#
		try:
			self.collection.drop()
			log(f'[  INFO  ] Collection - {self.faculty_id} dropped from Database - {config.Current_Batches_DB}')
			return 512
		except:
			log(f'[  ERROR ] API Failed to drop Collection - {self.faculty_id} from Database - {config.Current_Batches_DB}')
			return 400

	def show_all(self):
		# THIS METHOD DOESN'T TAKE ANY INPUT PARAMETER.
		# IT RETURNS THE LIST OF ALL THE AVAILABLE DOCUMENTS INSIDE
		# COLLECTION FOR WHICH THE CURRENT_BATCHES CONSTRUCTOR HAS BEEN
		# INITIALIZED.
		#		
		res = self.collection.find({})
		try:
			if res.count() > 0:
				response = {
					'status':302,
					'res':res
				}
			else:
				response = {
					'status':302,
					'res':{}
				}
			log(f'[  INFO  ] Showing all Batches from Collection - {self.faculty_id} in Database - {config.Current_Batches_DB}')
		except:
			response = {
				'status':598,
				'res':None
			}
			log(f'[  ERROR ] API Failed to show available Batches from Collection - {self.faculty_id} in Database - {config.Current_Batches_DB}')
		return response

	def __del__(self):
		try:
			self.client.close()
			log(f'[  INFO  ] Closing Established Connection with Collection - {self.faculty_id} in Database - {config.Current_Batches_DB}')
		except:
			log(f'[  ERROR ] API Failed to Close Established Connection with Collection - {self.faculty_id} in Database - {config.Current_Batches_DB}')

if __name__ == "__main__":
	# TEST CODE COMES HERE
	pass

