from django.db import models

# Create your models here.
from django.db import models


class Users(models.Model):
	avatar_url =models.TextField(max_length=100,blank=True)
	login_name= models.TextField(max_length=100,blank=True ,unique=True)
	url =models.TextField(max_length=100,blank=True)
	saved_time_stamp=models.DateTimeField(auto_now_add=True, blank=True)
	def __str__(self):
		return self.login_name


class Apicall(models.Model):
	time_stamp=models.DateTimeField(auto_now_add=True, blank=True)
	searched_string=models.TextField(max_length=100,blank=True)
	filter_string=models.TextField(max_length=100,blank=True)