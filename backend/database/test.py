if DEBUG_STATUS:
		# This code is used to perform some CRUD operations on API created above
		# You can comment this out if you wants to avoid its running
		# Enter testing code below END OF DEBUG CODE
		print('---------------------------------------------------------')
		print('[ INFO  ] Program running in Debug Mode')
		print('---------------------------------------------------------')
		print('\n[ INFO  ] Checking Faculty API')
		print('[ INFO  ] Inserting a Faculty Profile')
		faculty = faculty()
		faculty.insert(
			id='F364A',
			name={'f_name':'Deepali','m_name':'','l_name':'Virmani'},
			dob={ 'day':'04','month':'06','year':'1998' },
			phone_numbers=['011-27883979','7428306355'],
			email=['cse_hod@gmail.com'],
			subjects=['Networking','Machine Learning','Artificial Intelligence'],
			qualifications=['Btech CSE','Mtech CSE','Phd. AI'],
			time_table={
					'monday':['cse-a-2021','cse-b-2021','un-scheduled',
							'un-scheduled','cse-a-2021-lab','cse-a-2021',
							'un-scheduled'],
					'tuesday':['cse-a-2021','cse-b-2021','un-scheduled',
							'un-scheduled','cse-a-2021-lab','cse-a-2021',
							'un-scheduled'],
					'wednesday':['cse-a-2021','cse-b-2021','un-scheduled',
							'un-scheduled','cse-a-2021-lab','cse-a-2021',
							'un-scheduled'],
					'thursday':['cse-a-2021','cse-b-2021','un-scheduled',
							'un-scheduled','cse-a-2021-lab','cse-a-2021',
							'un-scheduled'],
					'friday':['cse-a-2021','cse-b-2021','un-scheduled',
							'un-scheduled','cse-a-2021-lab','cse-a-2021',
							'un-scheduled'],
					},
			classes=['cse-a-2012','cse-b-2021'],
			ratings='4.3'
			)
		# waiting for key dump to continue
		input(f'[ INFO  ] Check on MongoDB Server for any Insertion in {config.Faculty_Profile_Collection} Collection ')
		#
		print(f'[ INFO  ] Querying  in {config.Faculty_Profile_Collection} Collection ')
		res = faculty.query('faculty_id','F364A')
		print('[ INFO  ] Received Documents : ')
		print(res)
		#
		print('[ INFO  ] Checking Update Method')
		faculty.update('F364A','name',{'f_name':'Meenakshi','m_name':'','l_name':''})
		input(f'[ INFO  ] Check on MongoDB Server for any Updation in {config.Faculty_Profile_Collection} Collection ')
		#
		print(f'[ INFO  ] Removing Inserted Document from {config.Faculty_Profile_Collection} Collection')
		faculty.remove('faculty_id','F364A')
		input(f'[ INFO  ] Check on MongoDB Server for any Deletion in {config.Faculty_Profile_Collection} Collection ')
		#
		print('\n---------------------------------------------------------')
		print('[ INFO  ] Checking Student API')
		student = student()
		print('[ INFO  ] Inserting a Student Profile')
		student.insert(
			enrollment='03620802717',
			name={'f_name':'Prashant','m_name':'','l_name':'Varshney'},
			phone_numbers=['7428206355','7982068083'],
			email=['pv03158@gmail.com','varshney.prashant98@gmail.com'],
			father_name={'f_name':'Girish','m_name':'Chandra','l_name':'Varshney'},
			year_of_join='2017',
			year_of_pass='2021',
			programme='btech',
			branch='cse',
			section='a',
			gender='m',
			dob={ 'day':'04','month':'06','year':'1998' },
			temp_address='Samaypur, Delhi - 110042',
			perm_address='CD Block, Pitampura'
			)
		# waiting for key dump to continues
		input(f'[ INFO  ] Check on MongoDB Server for any Insertion in {config.Student_Profile_Collection} Collection ')
		#
		print(f'[ INFO  ] Querying  in {config.Student_Profile_Collection} Collection ')
		res = student.query('enrollment','03620802717')
		print('[ INFO  ] Received Documents : ')
		print(res)
		#
		print('[ INFO  ] Checking Update Method')
		student.update('03620802717','name',{'f_name':'Preeti','m_name':'','l_name':'Yadav'})
		input(f'[ INFO  ] Check on MongoDB Server for any Updation in {config.Student_Profile_Collection} Collection ')
		#
		print(f'[ INFO  ] Removing Inserted Document from {config.Student_Profile_Collection} Collection')
		student.remove('enrollment','03620802717')
		input(f'[ INFO  ] Check on MongoDB Server for any Deletion in {config.Student_Profile_Collection} Collection ')
		#
		print('\n---------------------------------------------------------')
		print('[ INFO  ] Checking Attendance API')
		attendance = attendance('F364A','btech','machine_learning','cse','a','5','2021')
		print('[ INFO  ] Inserting a Attendance Document')
		attendance.insert({
						'date':	{ 'day':'04','month':'06','year':'1998' },
						'attendance': {
								'03620802717':'P',
								'03720802717':'A',
								'05520802717':'P'
								}
						})
		input(f'[ INFO  ] Check on MongoDB Server for any Creation of Attendance Collection ')
		#
		print(f'[ INFO  ] Querying  in Attendance Collection ')
		res = attendance.show()
		print('[ INFO  ] Received Documents : ')
		print(res)
		#
		print(f'[ INFO  ] Querying  in Attendance Collection for date : 04-06-1998')
		res = attendance.show_on({ 'day':'04','month':'06','year':'1998' })
		print('[ INFO  ] Received Documents : ')
		print(res)

		print(f'[ INFO  ] Updation in Attendance Collection ')
		attendance.update(
						{ 'day':'04','month':'06','year':'1998' },
						{
						'date':	{ 'day':'04','month':'06','year':'1998' },
						'attendance': {
								'03620802717':'P',
								'03720802717':'P',
								'05520802717':'P'
									}
						})
		input(f'[ INFO  ] Check on MongoDB Server for any Updation in Attendance Collection ')
		print(f'[ INFO  ] Dropping Attendance Collection')
		attendance.remove()
		input(f'[ INFO  ] Check on MongoDB Server for any Deletion in Attendance Collection ')

		print('\n---------------------------------------------------------')
		print('[ INFO  ] Checking Marksheet API')
		marksheet = marksheet('F364A','btech','maths','cse','a','5','2021')
		print('[ INFO  ] Inserting a Marksheet Document')
		marksheet.insert({
						'enrollment':	'03720802717' ,
						'marks': '29',
						'assessment':'8'
						})
		input(f'[ INFO  ] Check on MongoDB Server for any Creation of Marksheet Collection ')

		print(f'[ INFO  ] Querying  in Marksheet Collection ')
		res = marksheet.show()
		print('[ INFO  ] Received Documents : ')
		print(res)

		print(f'[ INFO  ] Querying  in Marksheet Collection for enrollment: 03720802717')
		res = marksheet.show_on('03720802717')
		print('[ INFO  ] Received Documents : ')
		print(res)
		print(f'[ INFO  ] Updation in Marksheet Collection ')
		marksheet.update(
		 				 '03720802717',
		 				 {'enrollment':'03720802717',
						  'marks': '27',
						  'assessment':'8'
						  })
		input(f'[ INFO  ] Check on MongoDB Server for any Updation in Marksheet Collection ')
		print(f'[ INFO  ] Dropping Marksheet Collection')
		marksheet.remove('03720802717')
		input(f'[ INFO  ] Check on MongoDB Server for any Deletion in Marksheet Collection ')

  		print('\n---------------------------------------------------------------------')
		print('[ INFO  ] Checking Feedback API')
		feedback = feedback('A401', 'COA', 'B.tech', 'CSE', 'A', '3', '2021')
		print('[ INFO  ] Inserting a feedback document')
		feedback.insert({
			'date': {'day': '04', 'month': '06', 'year': '1998'},
			'enrollment': '05520802717',
			'feedback': 'nice work'
		}, '05520802717')
		input(f'[ INFO  ] Check on MongoDB Server for any creation of Feedback Collection ')
	
		print(f'[ INFO  ] Querying in Feedback Collection')
		res = feedback.show_all()
		print('[ INFO  ] Recieved Documents : ')
		print(res)

		print('[ INFO  ] Updation in Feedback Collection. ')
		feedback.update('05520802717', { 
				'date': {'day': '04' , 'month':'06','year':'2000'},
				'enrollment':'05520802717',
				'feedback': 'lol'
		 		})

		input(f'[ INFO  ] Check on MongoDB Server for any Updation in Feedback Collection ')
		print('[ INFO  ] Deleting a particular feedback ')
		feedback.remove_particular('05520802717')
		print('[ INFO  ] Feedback deleted of this student.')

		print('[ INFO  ] Dropping the feedback_sheet for the particular faculty. ')
		feedback.remove_all()
		print('[ INFO  ] Check on Mongo DB Server for any deletion in Feedback Collection.')
	################################ END OF DEBUG CODE ########################################
