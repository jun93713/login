# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.db import models

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class UserManager(models.Manager):
	def register(self, reg_info, request):
		validation = 'error'
		if len(reg_info['fname']) < 2 or len(reg_info['lname']) < 2:
			messages.error(request, 'names must be at least two characters!')
		elif not reg_info['fname'].isalpha() or not reg_info['lname'].isalpha():
			messages.error(request, 'names can only contain letters')
		elif not EMAIL_REGEX.match(reg_info['email']):
			messages.error(request, 'please enter email in correct format')
		elif len(reg_info['pss']) < 8:
			messages.error(request, 'password has to be at least 8 digits')
		elif reg_info['pss'] != reg_info['pssc']:
			messages.error(request, 'password has to match password confirmation')
		elif Users.objects.filter(email=reg_info['email']):
			messages.error(request, 'this email has been used')
		else:
			validation = 'valid'

		return validation

	def login(self, login_info, request):
		success = 'no'
		if Users.objects.filter(email=login_info['email']):
			if Users.objects.get(email=login_info['email']).password == login_info['pss']:
				success = 'yes'
			else:
				messages.error(request, 'wrong password')
		else:
			messages.error(request, 'user does not exist')

		return success

class Users(models.Model):
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	email = models.CharField(max_length=88)
	password = models.CharField(max_length=45)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()


