from django.shortcuts import render_to_response
from mainsite.users.forms import RegistrationForm
from mainsite.users.models import UserProfile
from django.views.generic.simple import direct_to_template
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from mainsite.settings import PROFILE_PIC_DIR, IMAGE_FILE_TYPES, IMAGE_MAX_SIZE
import os.path

def registration_page_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/dashboard/")
	path = request.get_full_path()
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username=form.cleaned_data['rno'], 
				email=form.cleaned_data['email'], 
				password=form.cleaned_data['pwd'],
				)
			user.first_name=form.cleaned_data['name']
			user.is_active=False;
			user.save()
			
			user_profile = UserProfile(
				name=form.cleaned_data['name'], 
				rno=form.cleaned_data['rno'], 
				email=form.cleaned_data['email'], 
				hostel=form.cleaned_data['email'], 
				cno=form.cleaned_data['cno'],
				profile_pic='default.png',
				)
			user_profile.active=False;
			user_profile.save()
			
			page_title = "Registration Successful"
			message = "Your Registartion Was Successful!"
		else:
			page_title = "Registration Unsuccessful"
			message = "Registration Failed!"
	else:	
		form = RegistrationForm()
		page_title = "Team Member Registration"
	return direct_to_template(request, 'users/register.html', locals())

def login(request):
	path = request.get_full_path()
	if request.user.is_authenticated():
		rno = request.POST.get('rno','')
		if rno != request.user.username and rno != '':						#To make sure there are valid logins if some tries to login using the browser back button while he is already logged in.
			auth.logout(request)
			pwd = request.POST.get('pwd','')
			user = auth.authenticate(username=rno, password=pwd)
			if user is not None:
				if(user.is_active):
					auth.login(request, user)
					return HttpResponseRedirect("/dashboard/")
				else:
					message = "You have not been activated."
			else:			
				message = "Roll No. and Password Do Not Match."
		else:
			return HttpResponseRedirect("/dashboard/")
	if request.method == "POST":
			rno = request.POST.get('rno','')
			pwd = request.POST.get('pwd','')
			user = auth.authenticate(username=rno, password=pwd)
			if user is not None:
				if(user.is_active):
					auth.login(request, user)
					return HttpResponseRedirect("/dashboard/")
				else:
					message = "You have not been activated."
			else:			
				message = "Roll No. and Password Do Not Match."
	return direct_to_template(request, 'users/login.html', locals())

def logout(request):
	if request.user.is_authenticated():
		auth.logout(request)
		message = "You were successfully logged out."
	return direct_to_template(request, 'users/login.html', locals())
		
def Profile(request):
	if not request.user.is_authenticated():
		message = "Login Before To Continue."
		return direct_to_template(request, 'users/login.html', locals())
	else:
		user_profile = UserProfile.objects.get(rno=request.user.username)
		if request.method == 'POST':
			message = ''
			name = request.POST.get('name','')
			email = request.POST.get('email','')
			hostel = request.POST.get('hostel','')
			cno = request.POST.get('cno','')
			pwd = request.POST.get('pwd','')
			re_pwd = request.POST.get('re_pwd','')
			if name.__len__() < 4:
				message = 'Please enter your actual name<br>'
			if email.__len__() < 12 or '@' not in email:
				message += 'Please provide a valid email<br>'
			if hostel.__len__() < 4 or hostel.__len__() > 15:
				message += 'No such hostel exists<br>'
			if cno.__len__() < 10:
				message += 'Invalid contact no.<br>'
			if re_pwd != '' and pwd != re_pwd:
				message += 'Passwords do not match<br>'		
			elif re_pwd != '' and pwd.__len__() < 6:
				message = 'Password should be minimum six characters'
			if message == '':
				UserProfile.objects.filter(rno=request.user.username).update(name=name,email=email,cno=cno,hostel=hostel)
				if re_pwd != '':
					request.user.set_password(pwd)
					request.user.save()
				message = 'Your profile was successfully updated!<br>'				
			if request.FILES.get('dp',''):
				profile_pic = request.FILES['dp']
				filename = profile_pic.name
				f, ext = os.path.splitext(filename)
				if ext not in IMAGE_FILE_TYPES:
					err_message = 'File Type Not Supported'
				elif profile_pic.size > IMAGE_MAX_SIZE:
					err_message = 'Maximum Allowed File Size is 2.5MB'
				else:
					fd = open('%s/%s' % (PROFILE_PIC_DIR, filename), 'wb')
					fd.write(profile_pic.read())
					fd.close()
					UserProfile.objects.filter(rno=request.user.username).update(profile_pic=filename)				
		user_profile = UserProfile.objects.get(rno=request.user.username)
		profile_pic = '/mainsite/media/uploads/dp/'+user_profile.profile_pic
		return direct_to_template(request, 'users/profile.html', locals())