import os
# This file contains all the configurations essential to connect to database and server
# Use this file to store keys of database, server, etc.
# And to apply that details import this file into your program as a module

MongoDB_URI = os.environ["MongoDB_URI"]

# Database Identifiers
Database_Name = "atom_db"
Attendance_DB = "attendance_db"
Batch_DB = "batch_db"
Current_Batches_DB = "current_batches_db"
Faculty_DB = "faculty_db"
Feedback_DB = "feedback_db"
Marksheet_DB = "marksheet_db"
Previous_Batches_DB = "previous_batches_db"
Student_DB = "student_db"
Provisional_Student_DB = "provisional_student_db"
Provisional_Faculty_DB = "provisional_faculty_db"
StudyMaterial_DB = "studymaterial_db"
Admin_DB = "admin_db"
OTP_DB = 'otp_db'

Faculty_Profile_Collection = "user_info"
Student_Profile_Collection = "user_info" 
Provisional_Student_Profile_Collection = "user_info" 
Provisional_Faculty_Profile_Collection = "user_info"
Admin_Profile_Collection = "user_info"
OTP_COLLECTION = "generated_otp"

SENDER_EMAIL_ID = os.environ["SENDER_EMAIL_ID"]
SENDER_EMAIL_PASSWORD = os.environ["SENDER_EMAIL_PASSWORD"]

SENDER_SMS_AUTH = os.environ["SENDER_SMS_AUTH"]