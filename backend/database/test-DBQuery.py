import DBQuery as db
import os
import sys
import random
import string
from datetime import datetime

## CREATING DUMMY OBJECTS FOR TESTING PURPOSE
SUBJECTS = ['machine_learning','artificial_intelligence','computer_networks','computer_architecture_and_organization',
            'electronic_devices','engineering_mathematics','engineering_mechanics','engineering_physics',
            'database_management','human_values_and_professional_ethics','communication_skills',
            'cryptocurrency','data_mining','java','c++','datastructures','engineering_drawing','engineering_chemistry',
            'web_development']
FACULTY_IDS = [ 'f'+'{num:03d}'.format(num=i)+'bpit' for i in range(1,100) ]
ENROLLMENT_NOS = [ "{enrollment:011d}".format(enrollment=int(suffix))
        for suffix in [ str(prefix)+'20802717' for prefix in range(0,5) ] ]
PROGRAMMES = ['btech','mtech','bca','mca','phd','bsc','msc']
BRANCHES = ['cse','ece','eee','it','mech']
SECTIONS = ['a','b','c','d','e']
YEAR_OF_PASS = list(range(2021,2025))
SEMESTERS = list(range(1,6))
MULTI_TEST_SiZE = 500
CLASS_STRENGTH = 200
MARKS = list(range(1,100))
ASSESSMENT = list(range(1,100))
NAMES = ['somya','preeti','tarun','prashant','lakshay','aakriti','shristi','shakira','dua-lipa','bebe-rexha','selena','alex','sommer-ray','pooja','minakshi','beyonce','nikki']
QUALIFICATIONS=['btech','mtech','bca','mca','phd','bsc','msc']
CLASSES = ['btech-cse-a-2021','btech-ece-a-2020','btech-cse-b-2021','btech-eee-a-2021','btech-it-a-2021','btech-mech-a-2020']
domains = [ "hotmail.com", "gmail.com", "aol.com", "mail.com" , "mail.kz", "yahoo.com","yahoo.co.in","icloud.com","outlook.com"]


def generate_dob_dictionary():
    day = random.randrange(1,32)
    month = random.randrange(1,13)
    year = random.randrange(1980,2000)
    return { 'day': day, 'month':month , 'year':year }

def generate_random_emails():
    # Generate a random string of letters and digits
    stringLength = random.randint(1,20)
    one_domain = random.choice(domains)
    lettersAndDigits = string.ascii_letters + string.digits
    one_name = str(''.join((random.choice(lettersAndDigits) for i in range(stringLength))))
    return (one_name + '@' + one_domain)

# FOR RANDOM PASSWORD GENERATION
# def generate_password(stringLength=10):
#     password_characters = string.ascii_letters + string.digits + string.punctuation
#     return ''.join(random.choice(password_characters) for i in range(stringLength))

def generate_attendance_dictionary(count=100):
    global ENROLLMENT_NOS
    date = datetime.now()
    day = date.strftime('%d')
    month = date.strftime('%m')
    year = date.strftime('%Y')
    dictionary_list = []
    for i in range(count):
        dictionary = {
            'date':{ 'day':str(int(day)+i),'month':month,'year':year },
            'attendance':{}
        }
        for j in ENROLLMENT_NOS:
            dictionary['attendance'][j] = random.choice(['P','A'])
        if count == 1:
            return dictionary
        else:
            dictionary_list.append(dictionary)
    return dictionary_list

def generate_feedback_dictionary(count = 100):
    date = datetime.now()
    day = date.strftime('%d')
    month = date.strftime('%m')
    year = date.strftime('%Y')
    dictionary_list = []
    for i in range(count):
        dictionary = {
            'date': { 'day':str(int(day)+i) , 'month':month , 'year':year },
            'enrollment' : random.choice(ENROLLMENT_NOS),
            'feedback' : {}
        }
        if count == 1:
            return dictionary
        else:
            dictionary_list.append(dictionary)
    return dictionary_list

def generate_markseet_dictionary(count = 100):
    dictionary_list = []
    for i in range(count):
        dictionary = {
            'enrollment' : random.choice(ENROLLMENT_NOS),
            'marks' : random.choice(MARKS),
            'assessment' : random.choice(ASSESSMENT)
        }
        if count == 1:
            return dictionary
        else:
            dictionary_list.append(dictionary)
    return dictionary_list


## CLI MAIN MENU
def main_menu():
    # CLEARING CONSOLE SCREEN
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    print("""
-------------------------------------------------------------------------------------------------------------------------------------
                                                            DBQuery Testing Script
-------------------------------------------------------------------------------------------------------------------------------------
                                                                                                        <c> Three Musketeers
1> Single Entry Test
2> Multiple Entry Test
3> Multiple Connection Test
4> Single Entry Test With Autonomous Checking
5> Multiple Entry Test With Autonomous Checking
6> Exit
""")

if __name__ == "__main__":
    main_menu()
    main_selection = int(input('[ Select Option ] '))
    if main_selection == 1:
        # PERFORMING SINGLE ENTRY TEST FOR ALL APIS
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        print("[  INFO  ] Starting Single Entry Testing Engine ")
        print("[  INFO  ] Testing Faculty API Functionality ")  
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        ######################################TESTING OF FACULTY API ######################################
        errors_list = []     
        faculty = db.Faculty()
        faculty_id = random.choice(FACULTY_IDS)     ## STORING RANDOMLY GENERATED ID IN VARIABLE TO FACILITATE THE FURTHER PROCESS OF QUERY
        print(f'[  INFO  ] Working on Faculty collection.')
        ##
        ## TESTING INSERTION METHOD ##
        status = faculty.insert(
            id=faculty_id,
            name=random.choice(NAMES),
            dob=generate_dob_dictionary(),
            phone_numbers=random.randrange(6111111111,10000000000),
            email=generate_random_emails(),
            password='faculty',
            subjects=random.choice(SUBJECTS),
            qualifications=random.choice(QUALIFICATIONS),
            time_table={},
            classes=random.choice(CLASSES),
            ratings=random.randint(1,5)
            )   
        print("[  INFO  ] Inserting Dummy Faculty in Faculty_DB ( Count : 1 )")
        print(f'[ STATUS ] {status}') 	## PRINTING STATUS OF RESULT OF QUERY
        ## SECOND ENTRY IN FACULTY_DB
        print("[  INFO  ] Inserting Dummy Faculty Dictionary in Faculty_DB ( Count : 2 )")
        status = faculty.insert(
            id=random.choice(FACULTY_IDS),
            name=random.choice(NAMES),
            dob=generate_dob_dictionary(),
            phone_numbers=random.randrange(6111111111,10000000000),
            email=generate_random_emails(),
            password='faculty',
            subjects=random.choice(SUBJECTS),
            qualifications=random.choice(QUALIFICATIONS),
            time_table={},
            classes=random.choice(CLASSES),
            ratings=random.randint(1,5)
            )   
        print(f'[ STATUS ] {status}') 	## PRINTING STATUS OF RESULT OF QUERY
        error_status = input("[  HALT  ] Check For Any Discrepancy In Faculty_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Faculty - Insertion Method')
        ##
        ## TESTING QUERY METHOD ##
        print('\n[  INFO  ] Querying The Faculty API.')
        response = faculty.query('faculty_id',faculty_id)
        print(f'[ STATUS ] { response["status"] }')
        print(*response['res'],sep='\n')
        error_status = input("[  HALT  ] Check For Any Discrepancy In Faculty_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Faculty - Query Method')
        ##
        ## TESTING UPDATE METHOD ##
        print(f'\n[  INFO  ] Updating Faculty API for {faculty_id}.')
        status = faculty.update(faculty_id,'name',random.choice(NAMES))
        print(f'[ STATUS ] { status }')            ## PRINTING STATUS OF RESULT OF QUERY
        error_status = input("[  HALT  ] Check For Any Discrepancy In Faculty_DB (Y/N) : ")
        if error_status in ['Y','y']:
            errors_list.append('Faculty - Update Method')
        ##
        ## TESTING REMOVE METHOD ##
        print(f'\n[  INFO  ] Removing Faculty_ID - { faculty_id } From Faculty_DB')
        status = faculty.remove('faculty_id',faculty_id)
        print(f'[ STATUS ] { status }')       ## PRINTING STATUS OF REMOVE METHOD
        error_status = input("[  HALT  ] Check For Any Discrepancy In Faculty_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Faculty - Remove Method')        
        ## LISTING ERRORS FOUND IN FACULTY API TEST ##
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        print('[  INFO  ] Errors In Faculty API : {} '.format(len(errors_list)))
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        print(*errors_list,sep='\n')
        ################################################# TESTING OF FACULTY API FINISHED #################################################

        ################################################# TESTING OF ATTENDANCE API STARTED ###############################################
        print('\n-------------------------------------------------------------------------------------------------------------------------------------')
        print("[  INFO  ] Testing Attendance API Functionality ")  
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        errors_list.clear()
        faculty_id=random.choice(FACULTY_IDS)
        subject=random.choice(SUBJECTS)
        programme=random.choice(PROGRAMMES)
        branch=random.choice(BRANCHES)
        section=random.choice(SECTIONS)
        year_of_pass=random.choice(YEAR_OF_PASS)
        semester=random.choice(SEMESTERS)
        ##
        attendance = db.Attendance(faculty_id,subject,programme,branch,section,year_of_pass,semester)
        print(f'[  INFO  ] Working On Collection : {faculty_id}_{subject}_{programme}_{branch}_{section}_{year_of_pass}_{semester}')
        ##
        ## TESTING INSERTION METHOD ##
        dictionary = generate_attendance_dictionary(2)  ## FIRST ENTRY IN ATTENDANCE_DB
        status = attendance.insert(dictionary[0])
        print("[  INFO  ] Inserting Dummy Attendance Dictionary in Attendance_DB ( Count : 1 )")
        print(f'[ STATUS ] {status}') 	## PRINTING STATUS OF RESULT OF QUERY
        status = attendance.insert(dictionary[1])   ## SECOND ENTRY IN ATTENDANCE_DB
        print("[  INFO  ] Inserting Dummy Attendance Dictionary in Attendance_DB ( Count : 2 )")
        print(f'[ STATUS ] {status}') 	## PRINTING STATUS OF RESULT OF QUERY
        error_status = input("[  HALT  ] Check For Any Discrepancy In Attendance_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Attendance - Insertion Method')
        dictionary = dictionary[0]      ## AS WE ARE GOING TO CHANGE FIRST INSERTED ELEMENT
        ## TESTING SHOW_ON METHOD ##
        print('\n[  INFO  ] Fetching Attendance Marked On {}/{}/{}'.format(dictionary['date']['day'],dictionary['date']['month'],dictionary['date']['year']))
        response = attendance.show_on(dictionary['date'])
        print(f'[ STATUS ] {response["status"]}')
        for res in response['res']:
            print(res['date'])
            for i in res['attendance']:
                print(i+':'+res['attendance'][i])
        error_status = input("[  HALT  ] Check For Any Discrepancy In Attendance_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Attendance - Show_On Method')
        ## TESTING SHOW_ALL METHOD ##
        print('\n[  INFO  ] Fetching Attendance Of All The Days ')
        response = attendance.show_all()
        print(f'[ STATUS ] {response["status"]}')
        for subres in response["res"]:
            print(subres['date'])
            for i in subres['attendance']:
                print(i+':'+subres['attendance'][i])
        error_status = input("[  HALT  ] Check For Any Discrepancy In Attendance_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Attendance - Show_All Method')
        ## TESTING UPDATE METHOD ##
        print('\n[  INFO  ] Updating Attendance Marked On {}/{}/{}'.format(dictionary['date']['day'],dictionary['date']['month'],dictionary['date']['year']))
        status = attendance.update(dictionary['date'],generate_attendance_dictionary(1))
        print(f'[ STATUS ] {status}') 	## PRINTING STATUS OF RESULT OF QUERY
        error_status = input("[  HALT  ] Check For Any Discrepancy In Attendance_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Attendance - Update Method')
        ## TESTING REMOVE_ALL METHOD ##
        print('\n[  INFO  ] Removing Dummy Attendance Sheet ')
        status = attendance.remove_all()
        print(f'[ STATUS ] {status}') 	## PRINTING STATUS OF RESULT OF QUERY
        error_status = input("[  HALT  ] Check For Any Discrepancy In Attendance_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Attendance - Remove_All Method')
        ## LISTING ERRORS FOUND IN ATTENDANCE API TEST ##
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        print('[  INFO  ] Errors In Attendance API : {} '.format(len(errors_list)))
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        print(*errors_list,sep='\n')
        ###################################### TESTING OF ATTENDANCE API FINISHED #############################################################

        ###################################### TESTING OF BATCH API STARTED ###################################################################
        print('\n-------------------------------------------------------------------------------------------------------------------------------------')
        print("[  INFO  ] Testing Batch API Functionality ")  
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        errors_list.clear()
        programme = random.choice(PROGRAMMES)
        branch = random.choice(BRANCHES)
        section = random.choice(SECTIONS)
        year_of_pass = random.choice(YEAR_OF_PASS)
        ##
        batch = db.Batch(programme,branch,section,year_of_pass)
        print(f'[  INFO  ] Working On Collection : {programme}_{branch}_{section}_{year_of_pass}\n')
        ##
        ## TESTING INSERT METHOD 
        for enrollment in ENROLLMENT_NOS:
            print(f'[  INFO  ] Inserting - {enrollment}')
            status = batch.insert(enrollment)
            print(f'[ STATUS ] {status}') 	## PRINTING STATUS OF INSERT METHOD
        enrollment = random.choice(ENROLLMENT_NOS)
        print(f'[  INFO  ] Trying To Insert Duplicate Entry - {enrollment}')
        status = batch.insert(enrollment)
        print(f'[ STATUS ] {status}')      ## PRINTING STATUS OF DUPLICATE INSERTION
        error_status = input("[  HALT  ] Check For Any Discrepancy In Batch_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Batch - Insert Method')
        ## TESTING SHOW_ALL METHOD 
        print('\n[  INFO  ] Fetching Enrollment Numbers Of Students Enrolled For The Current Batch')
        response = batch.show_all()
        print(f'[ STATUS ] {response["status"]}')
        print(*response['res'],sep='\n')
        error_status = input("[  HALT  ] Check For Any Discrepancy In Batch_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Batch - Show_All Method')
        ## TESTING REMOVE METHOD 
        enrollment = random.choice(ENROLLMENT_NOS)
        print(f'\n[  INFO  ] Removing Enrollment - {enrollment} From Batch_DB')
        status = batch.remove(enrollment)
        print(f'[ STATUS ] {status}')       ## PRINTING STATUS OF REMOVE METHOD
        error_status = input("[  HALT  ] Check For Any Discrepancy In Batch_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Batch - Remove Method')
        ## TESTING REMOVE_ALL METHOD 
        print('\n[  INFO  ] Removing Whole Collection ')
        status = batch.remove_all()
        print(f'[ STATUS ] {status}')
        error_status = input("[  HALT  ] Check For Any Discrepancy In Batch_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Batch - Remove_ALL Method')
        ## LISTING ERRORS FOUND IN BATCH API TEST ##
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        print('[  INFO  ] Errors In Batch API : {} '.format(len(errors_list)))
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        print(*errors_list,sep='\n')
        ################################################# TESTING OF BATCH API FINISHED ###########################################

        ################################################# TESTING OF FEEDBACK API STARTED ########################################
        print('\n-------------------------------------------------------------------------------------------------------------------------------------')
        print("[  INFO  ] Testing Feedback API")
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        errors_list.clear()
        faculty_id = random.choice(FACULTY_IDS)
        subject = random.choice(SUBJECTS)
        programme = random.choice(PROGRAMMES)
        branch = random.choice(BRANCHES)
        section = random.choice(SECTIONS)
        year_of_pass = random.choice(YEAR_OF_PASS)
        semester = random.choice(SEMESTERS)
        ##
        feedback = db.Feedback(faculty_id,subject,programme,branch,section,year_of_pass,semester)
        print(f'[  INFO  ] Working on COllection : {faculty_id}_{subject}_{programme}_{branch}_{section}_{year_of_pass}_{semester}\n')
        ##
        ## TESTING INSERT METHOD
        dictionary = generate_feedback_dictionary(2)         ## FIRST ENTRY IN FEEDBACK_DB
        status = feedback.insert(dictionary[0])
        print("[  INFO  ] Inserting Dummy Feedback Dictionary In Feedback_DB ( Count : 1 )")
        print(f'[ STATUS ] {status}')                      ## PRINTING STATUS RESULT OF QUERY
        status = feedback.insert(dictionary[1])         ## SECOND ENTRY IN FEEDBACK_DB
        print("[  INFO  ] Inserting Dummy Feedback Dictionary In Feedback_DB ( Count : 2 )")
        print(f'[ STATUS ] {status}')
        error_status = input("[  HALT  ] Check For Any Discrepancy In Feedback_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Feedback - Insertion Method')
        dictionary = dictionary[0]            ## AS WE ARE GOING TO CHANGE FIRST INSERTED ELEMENT
        ## TESTING SHOW_ALL METHOD 
        print("\n [  INFO  ] Fetching Feedback Of All The Days ")
        response = feedback.show_all()
        print(f'[ STATUS ] {response["status"]}')
        for subres in response['res']:
            print(subres['date'])
            print(subres['enrollment'])
            for i in subres['feedback']:
                print(i+':'+subres['feedback'][i])
        error_status = input("[  HALT  ] Check For Any Discrepancy In Feedback_DB (Y/N) : ")
        if error_status in ['Y','y']:
            errors_list.append('Feedback - Show_All Method ')
        ## TESTING UPDATE METHOD
        print('\n[  INFO  ] Updating Feedback {}'.format(dictionary['enrollment']))
        status = feedback.update(generate_feedback_dictionary(1))
        print(f'[ STATUS ] {status}')            ## PRINTING STATUS OF RESULT OF QUERY
        error_status = input("[  HALT  ] Check For Any Discrepancy In Feedback_DB (Y/N) : ")
        if error_status in ['Y','y']:
            errors_list.append('Feedback - Update Method')
        ## TESTING REMOVE METHOD 
        enrollment = random.choice(ENROLLMENT_NOS)
        print(f'\n[  INFO  ] Removing Enrollment - {enrollment} From Feedback_DB')
        status = feedback.remove(enrollment)
        print(f'[ STATUS ] {status}')           ## PRINTING STATUS OF REMOVE METHOD
        error_status = input("[  HALT  ] Check For Any Discrepancy In Feedback_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Feedback - Remove Method')
        ## TESTING REMOVE_ALL METHOD
        print('\n[  INFO  ] Removing Dummy Feedback Sheet')
        status = feedback.remove_all()
        print(f'[ STATUS ] {status}')          ## PRINTING STATUS OF RESULT OF QUERY
        error_status = input("[  HALT  ] Check For Any Discrepancy In Attendance_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Feedback - Remove_All Method')
        ## LISTING ERRORS FOUND IN ATTENDANCE API TEST ##
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        print('[  INFO  ] Errors In Attendance API : {} '.format(len(errors_list)))
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        print(*errors_list,sep='\n')
        ################################################# TESTING OF FEEDBACK API FINISHED #####################################

        ################################################ TESTING OF MARKSHEET API STARTED #######################################
        print('\n-------------------------------------------------------------------------------------------------------------------------------------')
        print('[  INFO  ] Testing Marksheet API')
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        errors_list = []
        faculty_id = random.choice(FACULTY_IDS)
        subject = random.choice(SUBJECTS)
        programme = random.choice(PROGRAMMES)
        branch = random.choice(BRANCHES)
        section = random.choice(SECTIONS)
        year_of_pass = random.choice(YEAR_OF_PASS)
        semester = random.choice(SEMESTERS)
        ##
        marksheet = db.Marksheet(faculty_id,subject,programme,branch,section,year_of_pass,semester)
        print(f'[  INFO  ] Working on collection : {faculty_id}_{subject}_{programme}_{branch}_{section}_{year_of_pass}_{semester}')
        ##
        ## TESTING INSERT METHOD
        dictionary = generate_markseet_dictionary(2)            ## FIRST ENTRY IN MARKSHEET_DB
        status = marksheet.insert(dictionary[0])
        print("[  INFO  ] Inserting Dummy Marksheet Dictionary in Marksheet_DB ( Count : 1 )")
        print(f'[  STATUS  ] {status}')                     ## PRINTING STATUS RESULT OF QUERY
        status = marksheet.insert(dictionary[1])            ## SECOND ENTRY IN MARKSHEET_DB
        print("[  INFO  ] Inserting Dummy Marksheet Dictionary in Marksheet_DB ( Count : 2 )")
        print(f'[  STATUS  ] {status}')
        error_status = input("[  HALT  ] Check For Any Discrepancy In Marksheet_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Marksheet - Insertion Method')
        dictionary = dictionary[0]            ## AS WE ARE GOING TO CHANGE FIRST INSERTED ELEMENT
        ## TESTING SHOW_OF METHOD
        print('\n[  INFO  ] Fetching Marksheet Of Enrollment {}'.format(dictionary['enrollment']))
        response = marksheet.show_of(dictionary['enrollment'])
        print(f'[ STATUS ] {response["status"]}')
        for res in response['res']:
            print(res['enrollment'])
            print(res['marks'])
            print(res['assessment'])
        error_status = input("[  HALT  ] Check For Any Discrepancy In Marksheet_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Marksheet - Show_Of Method')
        ## TESTING SHOW_ALL ME
        print('\n[  INFO  ] Fetching Marksheet Of All The Students.')
        response = marksheet.show_all()
        print(f'[  STATUS  ] {response["status"]}')
        for subres in response['res']:
            print(subres['enrollment'])
            print(subres['marks'])
            print(subres['assessment'])
        error_status = input("[  HALT  ] Check For Any Discrepancy In Marksheet_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Marksheet - Show_All Method')
        ## TESTING UPDATE METHOD
        print('\n[  INFO  ] Updating Marksheet {}'.format(dictionary['enrollment']))
        status = marksheet.update(dictionary['enrollment'],generate_markseet_dictionary(1))
        print(f'[  STATUS  ] {status}')                   ## PRINTING STATUS OF RESULT OF QUERY
        error_status = input("[  HALT  ] Check For Any Discrepancy In Marksheet_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Marksheet - Update Method')
        ## TESTING REMOVE METHOD
        enrollment = random.choice(ENROLLMENT_NOS)
        print(f'\n[  INFO  ] Removing Enrollment - {enrollment} From Marksheet_DB')
        status = marksheet.remove(enrollment)
        print(f'[ STATUS ] {status}')           ## PRINTING STATUS OF REMOVE METHOD
        error_status = input("[  HALT  ] Check For Any Discrepancy In Marksheet_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Marksheet - Remove Method')
        ## LISTING ERRORS FOUND IN MARKSHEET API TEST
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        print('[  INFO  ] Errors In Marksheet API : {} '.format(len(errors_list)))
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        print(*errors_list,sep='\n')
        ###################################################### TESTING OF MARKSHEET API FINISHED #####################################

        ###################################################### TESTING OF CURRENT_BATCHES API STARTED ################################
        print('\n-------------------------------------------------------------------------------------------------------------------------------------')
        print("[  INFO  ] Testing CURRENT_Batch API Functionality ")  
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        errors_list.clear()
        faculty_id = random.choice(FACULTY_IDS)
        subject = random.choice(SUBJECTS)
        semester = random.choice(SEMESTERS)
        programme = random.choice(PROGRAMMES)
        branch = random.choice(BRANCHES)
        section = random.choice(SECTIONS)
        year_of_pass = random.choice(YEAR_OF_PASS)
        current_batches = db.CurrentBatches(faculty_id)
        print(f'[  INFO  ] Working on collection : {faculty_id}\n')
        ## TESTING INSERT METHOD
        print(f'[  INFO  ] Inserting - {subject}_{semester}_{programme}_{branch}_{section}_{year_of_pass}')
        status = current_batches.insert(subject,semester,programme,branch,section,year_of_pass)
        print(f'[  STATUS  ] {status}')        ## PRINTING STATUS OF INSERT METHOD
        print(f'[  INFO  ] Trying To Insert Duplicate Entry - {subject}_{semester}_{programme}_{branch}_{section}_{year_of_pass}')
        status = current_batches.insert(subject,semester,programme,branch,section,year_of_pass)
        print(f'[  STATUS  ] {status}')        ## PRINTING STATUS OF DUPLICATE METHOD
        error_status = input("[  HALT  ] Check For Any Discrepancy In CurrentBatches_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Batch - Insert Method')
        ## TESTING SHOW_ALL METHOD
        print('\n[  INFO  ] Fetching all the batches of the faculty.')
        response = current_batches.show_all()
        print(f'[ STATUS ] {status}')
        error_status = input("[  HALT  ] Check For Any Discrepancy In CurrentBatches_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('CurrentBatches - Show_All Method')
        ## TESTING REMOVE METHOD
        print(f'[  INFO  ] Removing record of class from faculty class list.')
        status = current_batches.remove(programme,branch,section,year_of_pass)
        print(f'[ STATUS ] {status}')       ## PRINTING STATUS OF REMOVE METHOD
        error_status = input("[  HALT  ] Check For Any Discrepancy In CurrentBatches_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('CurrentBatches - Remove Method')
        ## TESTING REMOVE_ALL METHOD
        print('\n[  INFO  ] Removing Whole Collection.')
        status = current_batches.remove_all()
        print(f'[ STATUS ] {status}')
        error_status = input("[  HALT  ] Check For Any Discrepancy In CurrentBatches_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('CurrentBatches - Remove_ALL Method')
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        print('[  INFO  ] Errors In CurrentBatches API : {} '.format(len(errors_list)))
        print('-------------------------------------------------------------------------------------------------------------------------------------')
        print(*errors_list,sep='\n')
        ################################################### TESTING OF CURRENT_BATCHES API FINISHED #######################################

            
    elif main_selection == 2: 
        # PERFORMING MULTIPLE ENTRY TEST FOR ALL APIS
        print("[  INFO  ] Starting Multiple Entry Testing Engine ")
        print("[  INFO  ] Testing Attendance API Functionality ")  
        attendance = db.Attendance(
                faculty_id=random.choice(FACULTY_IDS),
                subject=random.choice(SUBJECTS),
                programme=random.choice(PROGRAMMES),
                branch=random.choice(BRANCHES),
                section=random.choice(SECTIONS),
                year_of_pass=random.choice(YEAR_OF_PASS),
                semester=random.choice(SEMESTERS)
            )
        for i in range(MULTI_TEST_SiZE):
            dictionaries = generate_attendance_dictionary(MULTI_TEST_SiZE)
            status = attendance.insert(dictionaries[i])
            print("\n[  INFO  ] Inserting Dummy Attendance Dictionary in Attendance_DB ( Count: {} ) ".format(i+1))
            print(f'[ STATUS ] {status}') 	# PRINTING STATUS OF RESULT OF QUERY
        input("[  HALT  ] Check For Any Discrepancy In Attendance_DB ")
        
    elif main_selection == 3:
        # PERFORMING MULTIPLE CONNECTION TEST
        pass
    elif main_selection == 4:
        # PERFORMING SINGLE ENTRY TEST WITH AUTONOMOUS CHECKING
        pass
    elif main_selection == 5:
        # PERFORMING MULTIPLE ENTRY TEST WITH AUTONOMOUS CHECKING
        pass
    else:
        print('Exiting...')
        sys.exit(0)