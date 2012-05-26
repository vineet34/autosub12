from django.db import models

class Assignment(models.Model):
	created_by = models.CharField(max_length=30)
	assg_status = models.CharField(max_length=10)
	assg_details = models.CharField(max_length=500)
	assg_title = models.CharField(max_length=60)
	creation_time = models.DateTimeField()
	assg_lock_datetime = models.DateTimeField()
	
	def __unicode__(self):
		return self.name
	
class Assg_Questions(models.Model):
	question = models.CharField(max_length=1000)
	ques_hint = models.CharField(max_length=100)
	assg_id = models.IntegerField(max_length=3)
	ques_file = models.FileField(upload_to='/media/')
	
	def __unicode__(self):
		return self.name
		
class Assg_Answers(models.Model):
	answer = models.CharField(max_length=1000)
	answer_by = models.CharField(max_length=8)
	ans_marks = models.IntegerField(max_length=3)
	ques_id = models.IntegerField(max_length=4)
	assg_id = models.IntegerField(max_length=3)
	ans_comments = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.name
		
class Assg_Stats(models.Model):
	assg_id = models.IntegerField(max_length=3)
	assg_student_rno = models.CharField(max_length=8)
	assg_student_name = models.CharField(max_length=30)
	assg_submit_time = models.DateTimeField()
	assg_solution_status = models.CharField(max_length=30)
	assg_comments = models.CharField(max_length=400)
	assg_marks = models.IntegerField(max_length=4)
	
	def __unicode__(self):
		return self.name
