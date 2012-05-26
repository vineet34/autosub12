from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=50)
    rno = models.CharField(max_length=8)
    email = models.EmailField()
    hostel = models.CharField(max_length=30)
    cno = models.CharField(max_length=15)
    pwd = models.CharField(max_length=128)
    active = models.BooleanField(default=False)
    profile_pic = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name