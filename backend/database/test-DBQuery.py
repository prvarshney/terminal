import DBQuery as db
import os
import sys
import random
from datetime import datetime

## CREATING DUMMY OBJECTS FOR TESTING PURPOSE
SUBJECTS = ['machine_learning','artificial_intelligence','computer_networks','computer_architecture_and_organization',
            'electronic_devices','engineering_mathematics','engineering_mechanics','engineering_physics',
            'database_management','human_values_and_professional_ethics','communication_skills',
            'cryptocurrency','data_mining','java','c++','datastructures','engineering_drawing','engineering_chemistry',
            'web_development']
FACULTY_IDS = [ 'F'+'{num:03d}'.format(num=i)+'BPIT' for i in range(1,100) ]
ENROLLMENT_NOS = [ "{enrollment:011d}".format(enrollment=int(suffix))
        for suffix in [ str(prefix)+'20802717' for prefix in range(0,5) ] ]
PROGRAMMES = ['btech','mtech','bca','mca','phd','bsc','msc']
BRANCHES = ['cse','ece','eee','it','mech']
SECTIONS = ['a','b','c','d','e']
YEAR_OF_PASS = list(range(2021,2025))
SEMESTERS = list(range(1,6))
MULTI_TEST_SiZE = 500
CLASS_STRENGTH = 200

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


## CLI MAIN MENU
def main_menu():
    # CLEARING CONSOLE SCREEN
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    print("""
----------------------------------------------------------------------------------------------------------
                                        DBQuery Testing Script
----------------------------------------------------------------------------------------------------------
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
        print('----------------------------------------------------------------------------------------------------------')
        print("[  INFO  ] Starting Single Entry Testing Engine ")
        print("[  INFO  ] Testing Attendance API Functionality ")  
        print('----------------------------------------------------------------------------------------------------------')
        ######################################### TESTING OF ATTENDANCE API STARTED ######################################################
        errors_list = []
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
        print('----------------------------------------------------------------------------------------------------------')
        print('[  INFO  ] Errors In Attendance API : {} '.format(len(errors_list)))
        print('----------------------------------------------------------------------------------------------------------')
        print(*errors_list,sep='\n')
        ###################################### TESTING OF ATTENDANCE API FINISHED #############################################################
        ###################################### TESTING OF BATCH API STARTED ###################################################################
        print('\n----------------------------------------------------------------------------------------------------------')
        print("[  INFO  ] Testing Batch API Functionality ")  
        print('----------------------------------------------------------------------------------------------------------')
        errors_list.clear()
        programme = random.choice(PROGRAMMES)
        branch = random.choice(BRANCHES)
        section = random.choice(SECTIONS)
        year_of_pass = random.choice(YEAR_OF_PASS)
        ##
        batch = db.Batch(programme,branch,section,year_of_pass)
        print(f'[  INFO  ] Working On Collection : {programme}_{branch}_{section}_{year_of_pass}\n')
        ##
        ############################################ TESTING INSERT METHOD ###################################################################
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
        ############################################# TESTING SHOW_ALL METHOD ###############################################################
        print('\n[  INFO  ] Fetching Enrollment Numbers Of Students Enrolled For The Current Batch')
        response = batch.show_all()
        print(f'[ STATUS ] {response["status"]}')
        print(*response['res'],sep='\n')
        error_status = input("[  HALT  ] Check For Any Discrepancy In Batch_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Batch - Show_All Method')
        ############################################# TESTING REMOVE METHOD #################################################################
        enrollment = random.choice(ENROLLMENT_NOS)
        print(f'\n[  INFO  ] Removing Enrollment - {enrollment} From Batch_DB')
        status = batch.remove(enrollment)
        print(f'[ STATUS ] {status}')       ## PRINTING STATUS OF REMOVE METHOD
        error_status = input("[  HALT  ] Check For Any Discrepancy In Batch_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Batch - Remove Method')
        ############################################# TESTING REMOVE_ALL METHOD #############################################################
        print('\n[  INFO  ] Removing Whole Collection ')
        status = batch.remove_all()
        print(f'[ STATUS ] {status}')
        error_status = input("[  HALT  ] Check For Any Discrepancy In Batch_DB (Y/N) : ")
        if error_status in ['y','Y']:
            errors_list.append('Batch - Remove_ALL Method')
        ## LISTING ERRORS FOUND IN BATCH API TEST ##
        print('----------------------------------------------------------------------------------------------------------')
        print('[  INFO  ] Errors In Batch API : {} '.format(len(errors_list)))
        print('----------------------------------------------------------------------------------------------------------')
        print(*errors_list,sep='\n')
        ###################################### TESTING OF BATCH API FINISHED #############################################################

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