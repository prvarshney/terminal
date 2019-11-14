from pymongo import MongoClient
from logger import log
import sys
import config

## START OF PREVIOUS_BATCHES API
## ------------------------------------------------------
## THIS API IS USED TO APPLY CRUD OPERATIONS ON THE BATCHES ANY FACULTY
## IS HAD PREVIOUSLY TOOK UNDER HIM/HER.
##
## THIS API IS USED FOR THE FOLLOWING FUNCTIONS:-
## 1. INSERTING DIFFERENT BATCHES THAT FACULTY HAS TOOK WITH METHOD NAME - INSERT
## 2. REMOVING THE PARTICULAR BATCH WITH METHOD NAME - REMOVE
## 3. REMOVING ALL THE BATCH FOR THE FACULTY WITH METHOD NAME - REMOVE_ALL
## 4. TO DISPLAY ALL THE BATCHES UNDER ANY FACULTY WITH METHOD NAME - SHOW_ALL
##
class PreviousBatches:
	def __init__(self, faculty_id):
		#CONSTRUCTOR OF PREVIOUS_BATCHES ACCEPTS THE FOLLOWING PARAMETERS:
		#FACULTY_ID --> UNIQUE ID FOR THE FACULTY --> STRING
		#
		#CREATING A COLLECTION IN DATABASE WITH IDENTIFIER LIKE :-
		#037_PREVIOUS_CLASSES
		# THIS COLLECTION OBJECT IS GONNA BE USED FOR FURTHER OPERATION LIKE-
		# INSERTING, UPDATING OR REMOVING THE SUBJECTS FROM THE FACULTY LIST.
		#
		try:
			self.client = MongoClient(config.MongoDB_URI)
			db = self.client[config.Previous_Batches_DB]
			log('[ INFO  ] Previous_Batches_DB Connected Successfully')
		except:
			log('[ Error ] Unable To Create Connection With Previous_Batches_DB')
			sys.exit(0)
		self.collection = db[f'{faculty_id}']

	def insert(self,subject,semester,programme,branch,section,year_of_pass):
		# PREVIOUS_CLASSES_DICTIONARY OBJECT CONTAINS A DICTIONARY THAT STORES THE PREVIOUS
		# SUBJECT WITH THE PREVIOUS SEMESTER AND THE PREVIOUS CLASS NAME AND BATCH.
		# ------------------------------------------------------------------------------------
		# DATA STRUCTURE OF INPUT PARAMETERS :-
		# SUBJECT --> STRING
		# SEMESTER --> STRING
		# PROGRAMME --> STRING
		# BRANCH --> STRING
		# SECTION --> STRING
		# YEAR_OF_PASS --> STRING
		#
		# CREATING DICTIONARY OF THE DOCUMENT THAT IS TO BE INSERTED IN DB.
		#
		previous_batches_dictionary = {
			"subject" : subject,
			"semester" : semester,
			"batch" : f'{programme}_{branch}_{section}_{year_of_pass}'
		}
		duplicate_entry = self.collection.find_one({'batch':previous_batches_dictionary['batch']})
		if duplicate_entry != None:
			log('[ ERROR ] This Batch Is Already Present In Database')
			return 417
		else:
			status = self.collection.insert_one(previous_batches_dictionary)
			log(f'[ INFO ] {status}') #PRINTING STATUS OF RESULT OF QUERY
			log('[ INFO  ] A previous batch is added in Previous_Batches_DB.')
			return 201

	def remove(self,programme,branch,section,year_of_pass):
		# THIS METHOD REMOVES THE RECORD OF THAT CLASS FROM THE FACULTY
		# PREVIOUS CLASS LIST.
		# ----------------------------------------------------------------------
		# DATA STRUCTURE OF INPUT PARAMETER:-
		# PREVIOUS_BATCH --> STRING
		#
		try:
			status = self.collection.delete_many(
				{ 'batch':f'{programme}_{branch}_{section}_{year_of_pass}' })
			log(f'[ INFO  ] {status}')      #PRINTING STATUS OF RESULT OF QUERY
			log('[ INFO  ] Record of particular class from Previous_Batches_DB has been successfully removed.')
			return 220
		except:
			return 203

	def remove_all(self):
		# THIS METHOD REMOVES ALL THE SUBJECTS AND CLASSES OF THE FACULTY.
		#  E.G. SUPPOSE A FACULTY LEAVES THE COLLEGE
		#  SO THERE IS NO NEED TO MAINTAIN THE PREVIOUS CLASS SHEET FOR THAT
		#  FACULTY.
		#
		try:
			self.collection.drop()
			log(f'[ INFO  ] Requested Collection Dropped')
			return 512
		except:
			return 400

	def show_all(self):
		# THIS METHOD DOESN'T TAKE ANY INPUT PARAMETER.
		# IT RETURNS THE LIST OF ALL THE AVAILABLE DOCUMENTS INSIDE
		# COLLECTION FOR WHICH THE PREVIOUS_CLASSES CONSTRUCTOR HAS BEEN
		#  INITIALIZED.
		#
		try:
			res = list(self.collection.find({}))
			log('[ INFO  ] All Collection of Previous_Classes has been displayed.')
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


	def __del__(self):
		self.client.close()


if __name__ == "__main__":
	# TEST CODE COMES HERE
	pass
