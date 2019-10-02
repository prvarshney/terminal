from pymongo import MongoClient
import sys
import config

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
			db = self.client[config.Current_Batches_DB]
			print('[ INFO  ] Current_Batches_DB Connected Successfully')
		except:
			print('[ Error ] Unable To Create Connection With Current_Batches_DB')
			sys.exit(0)
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
		current_batches_dictionary = {
			"subject" : subject,
			"semster" : semester,
			"batch" : f'{programme}_{branch}_{section}_{year_of_pass}'
		}
		duplicate_entry = self.collection.find_one({ 'batch':current_batches_dictionary['batch'] })
		if duplicate_entry != None:
			print('[ ERROR ] This Batch Is Already Present In Database For This Faculty')
			return 417
		else:
			status = self.collection.insert_one(current_batches_dictionary)
			print (f'[ INFO  ] {status}') #PRINTING STATUS OF RESULT OF QUERY
			return 201

	def remove(self,programme,branch,section,year_of_pass):
		# THIS METHOD REMOVES THE RECORD OF THAT CLASS FROM THE FACULTY
		# CURRENT CLASS LIST.
		# --------------------------------------------------------------
		# DATA STRUCTURE OF INPUT PARAMETER:-
		# CURRENT_BATCH --> STRING
		#
		try:
			status = self.collection.delete_many({ 'batch':
										f'{programme}_{branch}_{section}_{year_of_pass}' })
			print(f'[ INFO  ] {status}')
			return 220
		except:
			return 203

	def remove_all(self):
		# THIS METHOD REMOVES ALL THE BATCHES ANY FACULTY IS CURRENTLY TAKING.
		# FOR EXAMPLE : SUPPOSE ANY FACULTY LEAVES THE COLLEGE
		# 				SO THERE IS NO NEED TO MAINTAIN THE CURRENT CLASS
		# 				SHEET FOR THAT FACULTY.
		#
		try:
			self.collection.drop()
			return 512
		except:
			return 400

	def show_all(self):
		# THIS METHOD DOESN'T TAKE ANY INPUT PARAMETER.
		# IT RETURNS THE LIST OF ALL THE AVAILABLE DOCUMENTS INSIDE
		# COLLECTION FOR WHICH THE CURRENT_BATCHES CONSTRUCTOR HAS BEEN
		# INITIALIZED.
		#
		return list(self.collection.find({}))

	def __del__(self):
		self.client.close()


if __name__ == "__main__":
	# TEST CODE COMES HERE
	pass
