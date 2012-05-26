from django.shortcuts import render_to_response
from mainsite.users.models import UserProfile
from mainsite.Assignment.forms import AssignmentCreateForm, QuestionUploadForm
from mainsite.Assignment.models import Assignment, Assg_Questions, Assg_Answers, Assg_Stats
from django.views.generic.simple import direct_to_template
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from mainsite.settings import QUES_FILES_DIR, ALLOWED_FILE_TYPES, FILE_MAX_SIZE, ANS_FILES_DIR
from datetime import timedelta
import datetime
import os.path

def CreateAssignment(request):
	if request.user.is_authenticated():
		user_profile = UserProfile.objects.get(rno=request.user.username)
		if request.user.is_staff:
			form = AssignmentCreateForm(request.POST)
			students = User.objects.filter(is_staff=0)
			if	request.method == 'POST':
				if form.is_valid():
					try:
						t = request.POST['lock_dt_tm']
						y = int(t[6]+t[7]+t[8]+t[9])
						m = int(t[0]+t[1])
						d = int(t[3]+t[4])
						h = int(t[11]+t[12])
						mm = int(t[14]+t[15])
						lock_dt_tm = datetime.datetime(y,m,d,h,mm)
					except:
						for student in students:
							stu_id = str(student.id)
							if request.POST.get('cbx'+stu_id,''):
								student.cbx_chk = True
							else:
								student.cbx_chk = False
						message = "Invalid Date!"
						return direct_to_template(request, 'Assignment/create.html', locals())
					new_assg = Assignment(created_by=request.user.username,assg_status='Active',assg_details=request.POST['assg_details'],assg_title=request.POST['assg_title'],creation_time=datetime.datetime.now(),assg_lock_datetime=lock_dt_tm)
					new_assg.save()
					for student in students:
						stu_id = str(student.id)
						if request.POST.get('cbx'+stu_id,''):
							new_stat = Assg_Stats(assg_id=new_assg.id,assg_student_rno=student.username, assg_student_name=student.first_name, assg_solution_status='Pending', assg_submit_time='2099-12-31 23:59:59', assg_marks=-1)
							new_stat.save()
					create_success = True
					return direct_to_template(request, 'Assignment/create.html', locals())
				else:
					for student in students:
						stu_id = str(student.id)
						if request.POST.get('cbx'+stu_id,''):
							student.cbx_chk = True
						else:
							student.cbx_chk = False
					return direct_to_template(request, 'Assignment/create.html', locals())
			else:
				form = AssignmentCreateForm()
				req = request
				return direct_to_template(request, 'Assignment/create.html', locals())			
		else:		
			return HttpResponseRedirect("/dashboard/")
	else:
		return HttpResponseRedirect("/login/")

def AddQuestion(request, add_to):
	add_to = int(add_to)
	if request.user.is_authenticated():
		user_profile = UserProfile.objects.get(rno=request.user.username)
		if request.user.is_staff:
			assignment = Assignment.objects.filter(id=add_to)[0]
			if assignment.assg_status == 'Locked':
				assg_locked = True
				return direct_to_template(request, 'Assignment/add_question.html', locals())
			form = QuestionUploadForm(request.POST)
			if request.method == 'POST':
				if form.is_valid():
					filename = ''
					success_upload = False
					error_upload = False
					if request.FILES.get('ques_file',''):
						ques_file = request.FILES['ques_file']
						filename = ques_file.name
						f, ext = os.path.splitext(filename)
						if ext not in ALLOWED_FILE_TYPES:
							message = 'File Type Not Allowed'
							error_upload = True
						elif ques_file.size > FILE_MAX_SIZE:
							message = 'File size not to be more than 5MB'
							error_upload = True
						else:
							fd = open('%s/%s' % (QUES_FILES_DIR, filename), 'wb')
							fd.write(ques_file.read())
							fd.close()
							success_upload = True
					if not error_upload:
						if success_upload:
							new_ques = Assg_Questions(question=request.POST['question'],ques_hint=request.POST['ques_hint'],assg_id=request.POST['assg_select'],ques_file=filename)
						else:
							new_ques = Assg_Questions(question=request.POST['question'],ques_hint=request.POST['ques_hint'],assg_id=request.POST['assg_select'])
						new_ques.save()
						message = 'The Question Was Successfully Added.'
						form = QuestionUploadForm()
					assignments = Assignment.objects.filter(created_by=request.user.username).order_by('-id')
					return direct_to_template(request, 'Assignment/add_question.html', locals())
				else:
					assignments = Assignment.objects.filter(created_by=request.user.username).order_by('-id')
					return direct_to_template(request, 'Assignment/add_question.html', locals())
			else:
				form = QuestionUploadForm()
				assignments = Assignment.objects.filter(created_by=request.user.username).order_by('-id')
				return direct_to_template(request, 'Assignment/add_question.html', locals())
		else:
			return HttpResponseRedirect("/dashboard/")
	else:
		return HttpResponseRedirect("/login/")
			
	
def EditAssignment(request):
	if request.user.is_authenticated():
		user_profile = UserProfile.objects.get(rno=request.user.username)
		if request.user.is_staff:
			if request.method == 'POST':
				if request.POST['submit'] == 'Add Questions':
					return HttpResponseRedirect("/assignment/add/question/"+request.POST['edit_assg']+"/")
				elif request.POST['submit'] == 'Modify Assignment':
					return HttpResponseRedirect("/assignment/modify/"+request.POST['edit_assg']+"/")
				elif request.POST['submit'] == 'Delete Assignment':
					return HttpResponseRedirect("/assignment/delete/"+request.POST['edit_assg']+"/")
				else :
					return direct_to_template(request, 'Assignment/edit_assignment.html', locals())
			else:
				assignments = Assignment.objects.filter(created_by=request.user.username).order_by('-id')
				return direct_to_template(request, 'Assignment/edit_assignment.html', locals())
		else:
			return HttpResponseRedirect("/dashboard/")
	else:
		return HttpResponseRedirect("/login/")

def PreviewAssignment(request):
	if request.user.is_authenticated():
		user_profile = UserProfile.objects.get(rno=request.user.username)
		if request.method == 'POST':
			assg_id = request.POST['pvw_assg']
			assignments = Assignment.objects.order_by('-id')
			assg_to_pvw = Assignment.objects.filter(id=assg_id)
			questions = Assg_Questions.objects.filter(assg_id=assg_id)
			return direct_to_template(request, 'Assignment/preview_assignment.html', locals())
		else:
			assignments = Assignment.objects.order_by('-id')
			return direct_to_template(request, 'Assignment/preview_assignment.html', locals())
	else:
		return HttpResponseRedirect("/login/")

def DeleteAssignment(request, assg_id):
	if request.user.is_authenticated():
		user_profile = UserProfile.objects.get(rno=request.user.username)
		if request.user.is_staff:
			assignment = Assignment.objects.filter(id=assg_id)
			for assg in assignment:
				if assg.created_by != request.user.username:
					err_message = 'You are not privileged to delete this assignement.'
					return direct_to_template(request, 'Assignment/delete_assignment.html', locals())
				else:
					if assg.assg_status == 'Locked':
						err_message = 'You cannot delete this assignment as it has been locked.'
						return direct_to_template(request, 'Assignment/delete_assignment.html', locals())
					else:
						if request.method == 'POST':
							Assignment.objects.filter(id=assg_id).delete()
							err_message = 'The Assignment was successfully deleted'
							return direct_to_template(request, 'Assignment/delete_assignment.html', locals())							
						else:
							return direct_to_template(request, 'Assignment/delete_assignment.html', locals())
		else:
			return HttpResponseRedirect("/dashboard/")
	else:
		return HttpResponseRedirect("/login/")

def SolveAssignment(request):
	if request.user.is_authenticated():
		user_profile = UserProfile.objects.get(rno=request.user.username)
		if not request.user.is_staff or request.user.is_superuser:
			stats = Assg_Stats.objects.filter(assg_student_rno=request.user.username) #to populate the users assignment list
			assignments = Assignment.objects.all()
			if request.method == 'POST':
				assg = Assignment.objects.filter(id=request.POST.get('solve_assg',''))[0]
				solve_assg = request.POST.get('solve_assg','')
				questions = Assg_Questions.objects.filter(assg_id=solve_assg)
				stat = Assg_Stats.objects.filter(assg_student_rno=request.user.username, assg_id=assg.id)[0]
				if stat.assg_solution_status == 'SUBMITTED':
					submitted = True
					answers = Assg_Answers.objects.filter(assg_id=solve_assg, answer_by=request.user.username)
					message = 'You have successfully submitted this assignment at '+str(stat.assg_submit_time)
					return direct_to_template(request, 'Assignment/solve_assignment.html', locals())						
				if request.POST['submit'] == 'Solve':
					now = datetime.datetime.now()
					if  assg.assg_status == 'Active':
						if assg.assg_lock_datetime > now:
							answers = Assg_Answers.objects.filter(assg_id=solve_assg, answer_by=request.user.username)
						else:
							Assignment.objects.filter(id=request.POST.get('solve_assg','')).update(assg_status='Locked')
							assg_locked = True
					else:
						assg_locked = True
				elif request.POST['submit'] == 'Save':
					for question in questions:
						ans = request.POST.get('ans'+str(question.id),'')
						if ans:
							answer = Assg_Answers.objects.filter(assg_id=solve_assg, ques_id=question.id, answer_by=request.user.username)
							if answer.count():
								Assg_Answers.objects.filter(assg_id=solve_assg, ques_id=question.id, answer_by=request.user.username).update(answer=ans)
							else:
								Assg_Answers(assg_id=solve_assg, ques_id=question.id, answer_by=request.user.username, answer=ans, ans_marks=-1).save()								
							if request.FILES.get('ans_file_'+str(question.id),''):
								ans_file = request.FILES['ans_file_'+str(question.id)]
								f, ext = os.path.splitext(ans_file.name)
								f_err_message = ''
								if ext not in ALLOWED_FILE_TYPES or ans_file.size > FILE_MAX_SIZE:								
									if ext not in ALLOWED_FILE_TYPES :
										f_err_message += 'Question '+str(question.id)+' : File type not supported.<br>'
									if ans_file.size > FILE_MAX_SIZE:
										f_err_message += 'Question '+str(question.id)+' : Maximum file size allowed: 5MB<br>'	
								else:
									if not os.path.exists(ANS_FILES_DIR+'/'+request.user.username+'/'+solve_assg+'/'+str(question.id)+'/'):
										os.makedirs(ANS_FILES_DIR+'/'+request.user.username+'/'+solve_assg+'/'+str(question.id)+'/')
									fd = open('%s/%s' % (ANS_FILES_DIR+'/'+request.user.username+'/'+solve_assg+'/'+str(question.id)+'/', ans_file.name), 'wb')
									fd.write(ans_file.read())
									fd.close()
					answers = Assg_Answers.objects.filter(assg_id=solve_assg, answer_by=request.user.username)							
					message = 'Your answers were saved successfully!'
				elif request.POST['submit'] == 'Submit':
					Assg_Stats.objects.filter(assg_student_rno=request.user.username, assg_id=solve_assg).update(assg_solution_status='SUBMITTED',assg_submit_time=datetime.datetime.now())
					answers = Assg_Answers.objects.filter(assg_id=solve_assg, answer_by=request.user.username)
					submitted = True
					message = 'You have successfully submitted this assignment at '+str(stat.assg_submit_time)					
				#Populate the uploaded file list now in a dict.
				filedict = {'':''}				
				for question in questions:
					t_path = ANS_FILES_DIR+request.user.username+'/'+solve_assg+'/'+str(question.id)+'/'
					if os.path.exists(t_path):
						files = os.listdir(t_path)
						count = len(os.listdir(t_path))
						question.ansFileCount = range(count)
						question.hasAnsFiles = True
						counter = 0
						for file in files:
							filedict[str(question.id)+'_'+str(counter)+'_name'] = file
							filedict[str(question.id)+'_'+str(counter)+'_url'] = t_path+file
							counter += 1
					else:
						question.ansFileCount = 0
						question.hasAnsFiles = False						
				return direct_to_template(request, 'Assignment/solve_assignment.html', locals())
			else:
				return direct_to_template(request, 'Assignment/solve_assignment.html', locals())
		else:
			return HttpResponseRedirect("/dashboard/")
	else:
		return HttpResponseRedirect("/login/")
		
def dashboard(request):
	if not request.user.is_authenticated():
		message = "Login Before To Continue."
		return direct_to_template(request, 'users/login.html', locals())
	else:
		ref_dt_tm = datetime.datetime(2099,12,31,0,0)
		user_profile = UserProfile.objects.get(rno=request.user.username)
		assignments = Assignment.objects.all()
		for assignment in assignments:
			if User.objects.filter(username=assignment.created_by).count():
				assignment.created_by = User.objects.filter(username=assignment.created_by)[0].first_name
		stats = Assg_Stats.objects.filter(assg_student_rno=request.user.username)
		no_assg_total = 0
		no_assg_sub = 0
		for assignment in assignments:
			for stat in stats:
				if stat.assg_id == assignment.id:
					no_assg_total += 1
					if stat.assg_solution_status == 'SUBMITTED':
						no_assg_sub += 1
		return direct_to_template(request, 'users/dashboard.html', locals())

def ModifyAssignment(request, assg_id):
	if not request.user.is_authenticated():
		message = "Login Before To Continue."
		return direct_to_template(request, 'users/login.html', locals())
	else:
		if request.user.is_staff:
			assignment = Assignment.objects.filter(id=assg_id)[0]
			if not assignment.assg_status == 'Locked':
				students = User.objects.filter(is_staff=0)
				form = AssignmentCreateForm({'assg_title':assignment.assg_title,'assg_details':assignment.assg_details})
				for student in students:
					if Assg_Stats.objects.filter(assg_id = assg_id, assg_student_rno = student.username).count():
						student.cbx_chk = True
				if request.method == 'POST':
					if request.POST.get('lock_now',''):
						Assignment.objects.filter(id=assg_id).update(assg_status='Locked')
						assg_just_locked = True
						return direct_to_template(request, 'Assignment/modify.html', locals())
					assg_title = request.POST['assg_title']
					assg_details = request.POST['assg_details']
					modify_success = False
					if assg_title.__len__() < 6:
						message = "Title to be minimum six characters"
					elif assg_details.__len__() < 10:
						message = "Insufficient Details"
					else:
						modify_success = True
						Assignment.objects.filter(id=assg_id).update(assg_title=assg_title,assg_details=assg_details)
						message = 'Successfully modified the assignment.'				
					for student in students:
						stu_id = str(student.id)
						if not request.POST.get('cbx'+stu_id,''):
							Assg_Stats.objects.filter(assg_id=assg_id,assg_student_rno=student.username).delete()
							student.cbx_chk = False
						else: # overwrite or include new students, no students selected err
							if not Assg_Stats.objects.filter(assg_id=assg_id,assg_student_rno=student.username).count():
								new_stat = Assg_Stats(assg_id=assg_id,assg_student_rno=student.username, assg_student_name=student.first_name, assg_solution_status='Pending', assg_submit_time='2099-12-31 23:59:59', assg_marks=-1)
								new_stat.save()
								student.cbx_chk = True				
					try:
						t = request.POST['lock_dt_tm']
						y = int(t[6]+t[7]+t[8]+t[9])
						m = int(t[0]+t[1])
						d = int(t[3]+t[4])
						h = int(t[11]+t[12])
						mm = int(t[14]+t[15])
						lock_dt_tm = datetime.datetime(y,m,d,h,mm)
						Assignment.objects.filter(id=assg_id).update(assg_lock_datetime=lock_dt_tm)
					except:
						message = "Invalid Date!"
						return direct_to_template(request, 'Assignment/modify.html', locals())					
					assignment = Assignment.objects.filter(id=assg_id)[0]
					if modify_success:
						form = AssignmentCreateForm({'assg_title':assignment.assg_title,'assg_details':assignment.assg_details})
					else:
						form = AssignmentCreateForm(request.POST)
				lock_dt_tm = assignment.assg_lock_datetime
				if lock_dt_tm == datetime.datetime(2099,12,31,0,0):
					lock_dt_tm = datetime.datetime.now() + timedelta(days=3)
			else:
				assg_locked = True
				message = 'You cannot modify this assignment as it has been locked.'
			return direct_to_template(request, 'Assignment/modify.html', locals())
		else:
			return HttpResponseRedirect('/dashboard')
			
def DeleteFile(request, assg_id, qid, fname): 
	if request.user.is_authenticated():
		file = ANS_FILES_DIR+'/'+request.user.username+'/'+assg_id+'/'+str(qid)+'/'+fname
		folder = ANS_FILES_DIR+'/'+request.user.username+'/'+assg_id+'/'+str(qid)+'/'
		if os.path.exists(file):   #multiple requests to delete the same file
			os.remove(file)
		return direct_to_template(request, 'Assignment/file_deleted.html', locals())
	else:
		return HttpResponseRedirect('/login/')