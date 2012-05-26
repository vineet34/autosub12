from django import forms
from django.forms import ModelForm
from mainsite.users import models
from django.contrib.auth.models import User
import re

class RegistrationForm(ModelForm):
	name = forms.CharField(max_length=50, required=True, label='Full Name')
	rno = forms.CharField(max_length=8, min_length=8, required=True, label='Roll No.')
	email = forms.EmailField(max_length=50, required=True, label='Email')
	hostel = forms.CharField(max_length=20, required=True, label='Hostel')
	cno = forms.CharField(max_length=15, required=True, label='Contact No.')
	pwd = forms.CharField(min_length=6, widget=forms.PasswordInput, label='Password')
	re_pwd = forms.CharField(min_length=6, max_length=30, widget=forms.PasswordInput, label='Re-enter Password')
	
	class Meta:
		model = models.UserProfile
		fields = ('name','rno','email','hostel','cno','pwd','re_pwd')
	
	def clean_name(self):
		if not self.cleaned_data['name'].replace(' ','').isalpha():
			raise forms.ValidationError(u'Name Should Contain Only Letters.');
		else:
			return self.cleaned_data['name']
	def clean_rno(self):
		if User.objects.filter(username=self.cleaned_data['rno']):
			raise forms.ValidationError(u'You Are Already Registered')
		else:
			return self.cleaned_data['rno'].upper()
	def clean_email(self):
		if User.objects.filter(email=self.cleaned_data['email']):
			raise forms.ValidationError(u'You Are Already Registered')
		else:
			return self.cleaned_data['email']
	def clean_re_pwd(self):
		if self.cleaned_data['pwd'] != self.cleaned_data['re_pwd']:
			raise forms.ValidationError(u'Passwords Do Not Match.')
		else:
			return self.cleaned_data['pwd']