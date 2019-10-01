import DBQuery as db
import os
import sys
import random
import datetime

## CREATING DUMMY OBJECTS FOR TESTING PURPOSE
SUBJECTS = None
FACULTY_IDS = None
ENROLLMENT_NOS = [ "{enrollment:011d}".format(enrollment=int(suffix)) for suffix in [ str(prefix)+'20802717' for prefix in range(0,500) ] ]
PROGRAMMES = None
BRANCHES = None
SECTIONS = None
YEAR_OF_PASS = None
SEMESTERS = None

def generate_attendance_dictionary(count=100):
    

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
        print("[ INFO ] Starting Single Entry Testing Engine ")
        print("[ INFO ] Testing Attendance API Functionality ")  
        attendance = db.Attendance(
            faculty_id=random.choice(FACULTY_IDS)
            subject=random.choice(SUBJECTS)
            programme=random.choice(PROGRAMMES)
            branch=random.choice(BRANCHES)
            section=random.choice(SECTIONS)
            year_of_pass=random.choice(YEAR_OF_PASS)
            semester=random.choice(SEMESTERS)
        )
        dictionary = generate_attendance_dictionary(1)
        status = attendance.insert(dictionary)
        print("[ INFO ] Inserting the Following Attendance Dictionary in Attendance DB")
        print(dictionary)
        input("[ HALT ] Check For Any Discrepancy In Database ")

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