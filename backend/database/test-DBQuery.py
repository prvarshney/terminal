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
        for suffix in [ str(prefix)+'20802717' for prefix in range(0,500) ] ]
PROGRAMMES = ['btech','mtech','bca','mca','phd','bsc','msc']
BRANCHES = ['cse','ece','eee','it','mech']
SECTIONS = ['a','b','c','d','e']
YEAR_OF_PASS = list(range(2021,2025))
SEMESTERS = list(range(1,6))

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
        print("[  INFO  ] Starting Single Entry Testing Engine ")
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
        dictionary = generate_attendance_dictionary(1)
        status = attendance.insert(dictionary)
        print("\n[  INFO  ] Inserting Dummy Attendance Dictionary in Database")
        print(f'[ STATUS ] {status}') 	# PRINTING STATUS OF RESULT OF QUERY
        input("[  HALT  ] Check For Any Discrepancy In Database ")

    elif main_selection == 2:
        # PERFORMING MULTIPLE ENTRY TEST FOR ALL APIS
        pass
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