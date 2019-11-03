from pymongo import MongoClient
import config
import sys
from logger import log

## START OF BATCH COLLECTION API
## ------------------------------------------------------------------------------------------
## THIS BATCH CLASS IS USED FOR THE FOLLOWING FUNCTIONS:-
## 1. ADDING A NEW BATCH WITH METHOD NAME - INSERT
## 2. LISTING ALL THE STUDENTS ENROLLED IN A BATCH WITH METHOD NAME - SHOW_ALL
## 3. REMOVING ALL THE ENROLLED STUDENTS FROM BATCH WITH METHOD NAME - REMOVE_ALL
## 4. REMOVE ANY SINGLE STUDENT ENROLLED WITH METHOD NAME - REMOVE
##
class Batch:
	def __init__(self,programme,branch,section,year_of_pass):
		# THIS CONSTRUCTOR IS USED TO CREATE A REQUIRED COLLECTION
		# IN DATABASE. FOR EXAMPLE :- BATCH_BTECH_CSE_A_2021
		#
		self._programme = programme
		self._branch = branch
		self._section = section
		self._year_of_pass = year_of_pass
		try:
			self.client = MongoClient(config.MongoDB_URI)
			db = self.client[config.Batch_DB]
			log(f'[  INFO  ] {config.Batch_DB} Connected Successfully')
		except:
			log(f'[  ERROR ] Unable To Create Connection With {config.Batch_DB}')
		self.collection = db[ f'{programme}_{branch}_{section}_{year_of_pass}' ]

	def insert(self,enrollment):
		# USED TO INSERT ENROLLMENT OF A STUDENT IN THE REQUIRED COLLECTION
		# ---------------------------------------------------------------------------
		# DATA STRUCTURES OF ENROLLED_STUDENTS :-
		# ENROLLMENT --> STRING
		#
		# CHECKING FOR ANY DUPLICATE ENTRY IN THE COLLECTION
		duplicate_entry = self.collection.find_one({ 'enrollment':enrollment })
		if duplicate_entry != None:
			log(f'[  ERROR ] {enrollment} Enrollment Insertion at {self._programme}_{self._branch}_{self._section}_{self._year_of_pass} Collection in Batch_DB failed - Duplicate Entry Found')
			return 417
		else:
			status = self.collection.insert_one({ 'enrollment':enrollment })
			log(f'[  INFO  ] {status}')
			log(f'[  INFO  ] {enrollment} Enrollment Inserted Successfully at {self._programme}_{self._branch}_{self._section}_{self._year_of_pass} Collection in {config.Batch_DB}')
			return 201

	def remove(self,enrollment):
		# USED TO REMOVE ENROLLMENT OF A PARTICULAR STUDENT FROM BATCH COLLECTION
		# ----------------------------------------------------------------------------
		# DATA STRUCTURES OF INPUT PARAMETER :-
		# ENROLLMENT --> STRING
		#
		try:
			status = self.collection.delete_one({ 'enrollment':enrollment })
			log(f'[  INFO  ] {status}')
			log(f'[  INFO  ] {enrollment} Enrollment Removed From {self._programme}_{self._branch}_{self._section}_{self._year_of_pass} Collection in Batch_DB')
			return 220
		except:
			return 203
			log(f'[  ERROR ] Unable To Remove {enrollment} Enrollment From {self._programme}_{self._branch}_{self._section}_{self._year_of_pass} Collection in Batch_DB')
    
	def remove_all(self):
		# USED TO REMOVE WHOLE COLLECTION FOR WHICH BATCH CLASS
		# OBJECT IS INITIALISED.
		# ----------------------------------------------------------------------------
		#
		try:
			self.collection.drop()
			log(f'[  INFO  ] {self._programme}_{self._branch}_{self._section}_{self._year_of_pass} Collection Removed From Batch_DB')
			return 512
		except:
			log(f'[  ERROR ] Unable To Remove {self._programme}_{self._branch}_{self._section}_{self._year_of_pass} Collection From Batch_DB')
			return 400


	def show_all(self):
		# USED TO DISPLAY A LIST OF ALL THE ENROLLED STUDENTS IN A CLASS
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
					'res':{}
				}
			log(f'[  INFO  ] {self._programme}_{self._branch}_{self._section}_{self._year_of_pass} Collection Fetched From Batch_DB')
		except:
			response = {
				'status':598,
				'res':None
			}
			log(f'[  ERROR ] Unable To Fetch {self._programme}_{self._branch}_{self._section}_{self._year_of_pass} Collection From Batch_DB')
		return response

	def __del__(self):
		# log('[  INFO  ] Connection closed successfully of Batch_DB.')
		self.client.close()	# RELEASING OPEN CONNECTION WITH DATABASE


if __name__ == "__main__":
	# TESTING SCRIPT
	pass
