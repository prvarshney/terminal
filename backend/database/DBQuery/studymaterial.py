from pymongo import MongoClient
import sys
import config

## START OF STUDYMATERIAL COLLECTION API
## --------------------------------------------------------------------------
## THIS CLASS IS USED FOR THE FOLLOWING FUNCTIONS:-
## 1. INSERT NOTES/ASSIGNMENT WITH METHOD NAME - INSERT
## 2. SHOW WHOLE NOTES/ASSIGNMENT COLLECTION WITH METHOD NAME - SHOW_ALL
## 3. REMOVE WHOLE STUDYMATERIAL COLLECTION WITH METHOD NAME - REMOVE_ALL
## 5. REMOVE A PARTICULAR NOTES/ASSIGNMENT OF ANY PARTICULAR TITLE WITH METHOD NAME - REMOVE
##
class StudyMaterial:
	def __init__(self,faculty_id,subject,programme,branch,section,year_of_pass,semester):
		# CONSTRUCTOR OF STUDYMATERIAL ACCEPTS THE FOLLOWING PARAMETERS :
		# FACULTY_ID --> UNIQUE_ID OF FACULTY --> STRING
		# SUBJECT --> STRING
		# PROGRAMME --> PROGRAMME OF CLASS WHOSE ATTENDANCE NEEDS TO MARK LIKE BBA, BTECH --> STRING
		# BRANCH --> LIKE CSE, IT, ETC. --> STRING
		# SECTION --> STRING
		# YEAR_OF_PASS --> STRING
		# SEMESTER --> STRING
		#
		# CREATING A COLLECTION IN DATABASE WITH IDENTIFIER LIKE 036_STUDY_MATERIAL_BTECH_JAVA_A_5_2021
		# THIS COLLECTION OBJECT IS GONNA BE USED FURTHER FOR ANY OPERATION LIKE :-
		# INSERTING NOTES, SHOW_ALL, ETC.
		#
		try:
			self.client = MongoClient(config.MongoDB_URI)
			db = self.client[config.StudyMaterial_DB]
			print('[ INFO  ] StudyMaterial_DB Connected Successfully')
		except:
			print('[ Error ] Unable To Create Connection With StudyMaterial_DB')
		self.collection = db[f'{faculty_id}_{subject}_{programme}_{branch}_{section}_{year_of_pass}_{semester}']

	def insert(self,title,date,path):
		# THIS METHOD IS USED TO INSERT ABSOLUTE PATH OF NOTES/ASSIGNMENT DOCUMENT
		# IN THE SERVER.
		# -------------------------------------------------------------------------
		# DATASTRUCTURES OF THE INPUT PARAMETERS ARE :
		# TITLE --> STORES THE TITLE OF THE NOTE --> STRING
		# DATE --> STORES THE DATE ON WHICH NOTE IS STORED ON DATABASE --> DICTIONARY
		# PATH --> PATH OF THE NOTE/ASSIGNMENT FILE STORED IN DATABASE --> STRING
		#
		# HERE PRIMARY KEY IS PATH OF THE NOTES/ASSIGNMENT
		duplicate_entry = self.collection.find_one({ 'path':path })		# CHECKS WHETHER THE PATH OF NOTES IS ALREADY IN DB
		if duplicate_entry != None:
			print('[ Error ] Object of this title already present in Database')
			return 417
		else:
			status = self.collection.insert_one({
				'date': date,
				'title':title,
				'path':path
				})
			print(f'[ INFO  ] {status}')
			return 201

	def show_all(self):
		# THIS METHOD USED TO FETCH WHOLE COLLECTION OF STUDYMATERIAL
		# IT DOESN'T INPUTS ANY PARAMETER AND RETURNS A LIST OF DICTIONARIES
		#
		try:
			res = list(self.collection.find({}))
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


	def remove(self,title):
		# THIS METHOD USED TO REMOVE A DOCUMENT FROM STUDY_MATERIAL COLLECTION OF THE
		# BASIS OF TITLE.
		# -------------------------------------------------------------------------------
		# DATA STRUCTURE OF INPUT PARAMETER :
		# TITLE --> STRING
		#
		try:
			status = self.collection.delete_many({ 'title':title })
			print(f'[ INFO  ] {status}')
			return 220
		except:
			return 203


	def remove_all(self):
		# THIS METHOD REMOVES WHOLE COLLECTION OF THAT FACULTY STUDYMATERIAL COLLECTION
		# FOR WHICH ITS OBJECT IS INITIALISED.
		#
		try:
			status = self.collection.drop()
			return 512
		except:
			return 400

	def __del__(self):
		self.client.close()

if __name__== "__main__":
	# TEST CODE COMES HERE
	pass
