from pymongo import MongoClient
import sys
import config
from logger import log

## START OF FEEDBACK COLLECTION API
## ------------------------------------------------------------------------------------------
## THIS FEEDBACK CLASS IS USED FOR THE FOLLOWING FUNCTIONS:-
## 1. ADDING A FEEDBACK FOR A PARTICULAR TEACHER WITH METHOD NAME - INSERT
## 2. LISTING ALL THE FEEDBACKS OF A TEACHER WITH METHOD NAME - SHOW_ALL
## 3. REMOVING ALL THE FEEDBACK OF A TEACHER WITH METHOD NAME - REMOVE_ALL
## 4. REMOVE FEEDBACK BY A PARTICULAR STUDENE WITH METHOD NAME - REMOVE
##
class Feedback:
	def __init__(self,faculty_id,subject,programme,branch,section,year_of_pass,semester):
		# CONSTRUCTOR OF FEEDBACK ACCEPTS THE FOLLOWING PARAMETERS:-
		# FACULTY_ID --> UNIQUE_ID OF FACULTY --> STRING
		# SUBJECT --> MATHEMATICS, COA, ETC. --> STRING
		# PROGRAMME --> E.G. BTECH, BBA, ETC. --> STRING
		# BRANCH --> LIKE CSE, ECE, ETC. --> STRING
		# SECTION --> STRING
		# YEAR_OF_PASS --> STRING
		# SEMESTER --> STRING
		#
		# CREATING A COLLECTION IN DATABASE WITH IDENTIFIER LIKE :-
		# "F034A_COA_BTECH_CSE_A_2021_4"
		#
		# THIS COLLECTION OBJECT IS GONNA BE USED FURTHER FOR ANY OPERATION LIKE:-
		# ADDING THE FEEDBACK, SHOW_ALL,ETC.
		try:
			self.client = MongoClient(config.MongoDB_URI)
			db = self.client[config.Feedback_DB]
			log('[ INFO  ] Feedback_DB Connected Successfully')
		except:
			log('[ Error ] Unable To Create Connection With Feedback_DB')
			sys.exit(0)
		self.collection = db[f'{faculty_id}_{subject}_{programme}_{branch}_{section}_{year_of_pass}_{semester}']

	def insert(self,feedback_dictionary):
		# THIS METHOD IS USED TO ADD A FEEDBACK OF ANY FACULTY BY A PARTICULAR CLASS.
		# FEEDBACK_DICTIONARY IS A DICTIONARY, THAT STORES DATE ON WHICH THE
		# FEEDBACK WAS GIVEN, ENROLLMENT OF STUDENT THAT GIVES FEEDBACK,
		# AND THE FEEDBACK.
		# FOR EXAMPLE:
		# FEEDBACK_DICTIONARY = {
		#                       'DATE': { 'DAY': '07','MONTH':'11','YEAR':'2000' },
		#                       'ENROLLMENT': '03620802717',
		#                       'FEEDBACK': 'BEST TEACHER'
		#                       }
		#
		duplicate_entry = self.collection.find_one({ 'enrollment':feedback_dictionary['enrollment'] })
		if duplicate_entry != None:
			log('[ ERROR ] Feedback Of This Student Already Present In Database For This Faculty')
			return False
		else:
			status = self.collection.insert_one(feedback_dictionary)
			log (f'[ INFO  ] {status}') #PRINTING STATUS OF RESULT OF QUERY
			log('[ INFO  ] Feedback successfully inserted in Feedback_DB.')
			return True

	def show_all(self):
		# THIS METHOD DOESN'T INPUTS ANY PARAMETER AND RETURNS A LIST OF ALL THE
		# AVAILABLE DOCUMENTS INSIDE COLLECTION FOR WHICH THE FEEDBACK CONSTRUCTOR IS INITIALIZED.
		# THIS METHOD DISPLAYS ALL THE FEEDBACKS OF A PARTICULAR FACULTY GIVEN BY A PARTICULAR CLASS
		# STUDENT
		#
		return list(self.collection.find({}))
		log('[ INFO  ] All feedbacks of the faculty has been displayed.')

	def remove_all(self):
		# THIS METHOD REMOVES THE COLLECTION OF FEEDBACK OF THAT PARTICULAR FACULTY_ID FOR
		# WHICH CLASS OBJECT IS INITIALIZED.
		# FOR EXAMPLE:- IF ANY TEACHER HAS LEFT, THEN ALL THE FEEDBACKS OF THAT PARTICULAR
		# FACULTY MUST BE DELETED.
		#
		self.collection.drop()
		log(f'[ INFO  ] Requested Collection Dropped')

	def remove(self,enrollment):
		# THIS METHOD IS USED TO REMOVE THE FEEDBACK BY A STUDENT FOR A PARTICULAR FACULTY.
		#
		status = self.collection.delete_one({ 'enrollment':enrollment })
		log(f'[ INFO  ] {status}')
		log('[ INFO  ] Feedback of a particular student for a particular faculty has been removed.')

	def update(self,feedback_dictionary):
		# THIS UPDATE METHOD INPUTS THE FEEDBACK_DICTIONARY TO CHECK WHICH DOCUMENT NEEDS
		# TO BE UPDATED AND THEN, UPDATES IT.
		#
		searching_values = { 'enrollment':feedback_dictionary['enrollment'] }
		updating_values = feedback_dictionary
		try:
			status = self.collection.update_one(searching_values, {'$set':updating_values})
			log(f'[ INFO  ] {status}')
			log('Faculty_DB has been updated successfully.')
			return True
		except:
			log('[ ERROR  ] Faculty_DB failed to update.')
			return False

	def __del__(self):
		self.client.close()

if __name__ == "__main__":
	# TEST CODE COMES HERE
	Feedback = Feedback(faculty_id="06A",
	subject="toc",
	programme="btech",branch="cse",
	section="A",year_of_pass="2021",
	semester="five")
	Feedback.show_all()
	Feedback.remove('05520802717')
	Feedback.remove_all()
	Feedback.insert({
		'date':{'day':'06','month':'08','year':'2008'},
		'enrollment':'05530802717',
		'feedback':'best teacher'
	})
	Feedback.show_all()
	pass