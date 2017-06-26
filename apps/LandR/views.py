# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Users
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
	if 'status' not in request.session:
		request.session['status'] = ""
	if 'email' not in request.session:
		request.session['email'] = ""
	return render(request, 'LandR/index.html')

def regi(request):
	if 'error' in Users.objects.register(request.POST, request):
		return redirect('/')
	else:
		Users.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=request.POST['pss'])
		request.session['states'] = 'registered'
		request.session['email'] = request.POST['email']
		return redirect('/success')

def login(request):
	if 'no' in Users.objects.login(request.POST, request):
		return redirect('/')
	else:
		request.session['states'] = 'logged in'
		request.session['email'] = request.POST['email']
		return redirect('/success')

def success(request):

	context = {
		'name': Users.objects.get(email=request.session['email']).first_name,
		'status': request.session['states']
	}
	return render(request, 'LandR/success.html', context)