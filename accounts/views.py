import hashlib
import random
import re
import uuid
from django.shortcuts import render
from accounts.models import robodarshanMember, Profile
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.urlresolvers import reverse
from django.conf import settings
from accounts import forms

from accounts.tasks import send_mail_task


def register(request):
	if request.user.is_authenticated():
			return HttpResponseRedirect(reverse('accounts:profile'))
	if request.method == 'POST': # data has been submitted
		form = forms.RegistrationForm(request.POST)
		if form.is_valid():
			# Create the user
			form.clean()
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user = robodarshanMember.objects.create_user(email, password)
			user.fullname = form.cleaned_data['fullname']
			# Creat the verification key
			salt = hashlib.sha1(str(random.random())).hexdigest()[:10]
			email_verification_key = hashlib.sha1(salt+email).hexdigest()
			user.profile.email_verify_key = email_verification_key
			user.profile.save()
			user.save()
			mail_subject = 'Account verification'
			mail_body = settings.HOST_BASE_URL +  u'accounts/verify/' + email_verification_key + '?u=' + user.profile.uuid
			send_mail_task.delay( mail_subject, mail_body, 'ghoshbinayak@gmail.com', [email])
			return render(request, 'accounts/register.html', {'success': 'Registration Complete. Check your mailbox for instructions to verify your email accout.'})
		else:
			return render(request, 'accounts/register.html', {'form': form})
	else: # data not submitter just display the form
		form = forms.RegistrationForm()
		return render(request, 'accounts/register.html', {'form': form})

# Email verification

def verify(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('accounts:profile'))
	uuid = request.GET.get('u', False)
	email_verification_key = re.search(r'verify/(?P<email_verification_key>[0-9a-f]{40}$)', request.path)
	if uuid and email_verification_key:	
		email_verification_key = email_verification_key.groupdict().get('email_verification_key', False)
		try:
			user = Profile.objects.get(uuid = uuid).user
		except Profile.DoesNotExist:
			return render(request, 'accounts/verify.html', {'error': 'The email address is not registered'})
		else:
			if user.profile.email_verify_key == 'ACTIVATED':
				return render(request, 'accounts/verify.html', {'success': 'Your email is already verified. :)'})
			else:	
				if user.profile.email_verify_key == email_verification_key:
					user.profile.email_verify_key = 'ACTIVATED'
					user.profile.save()
					user.is_active = True
					user.save()
					return render(request, 'accounts/verify.html', {'success': 'successfully verified'})
				else:
					return render(request, 'accounts/verify.html', {'success': 'invalid verification key'})
	else:
		return render(request, 'accounts/verify.html', {'error': 'That doesn\'t seem quite right. Please ckeck the if you have copied the link correctly. '})


def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('accounts:profile'))
	if request.method == 'POST': # then login the user
		form = forms.LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			user = authenticate(email=email, password= password)
			if user is not None:
				if user.is_active:
					django_login(request, user)
					if request.POST.has_key('next'):
						return HttpResponseRedirect(request.POST['next'])
					return HttpResponseRedirect(reverse('accounts:profile'))
				else:
					return render(request, 'accounts/login.html', {'error': 'Your account is not active.'})
			else:
				form = forms.LoginForm()
				templateVars = {'form': form, 'error': 'wrong email or password.'}
				if request.POST.has_key('next'):
					templateVars['next'] = request.POST['next']
				return render(request, 'accounts/login.html', templateVars)
	else: # display login form
		form = forms.LoginForm()
		templateVars = {'form': form, 'next': reverse('accounts:profile')}
		if request.GET.has_key('next'):
			templateVars['next'] = request.GET['next']
		return render(request, 'accounts/login.html', templateVars)

def logout(request):
	django_logout(request)
	return HttpResponseRedirect(reverse('accounts:profile'))
	
def profile(request):
	if request.user.is_authenticated():
		return render(request, 'accounts/profile.html')
	else:
		return HttpResponseRedirect(reverse('accounts:login'))

def forgot(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('accounts:profile'))
	if request.method == 'POST': # then send password reset email
		form = forms.ForgotForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			try:
				user = robodarshanMember.objects.get(email = email) 
				if user.is_active:
					mail_subject = 'Password reset'
					salt = hashlib.sha1(str(random.random())).hexdigest()
					uid = hashlib.sha1(str(uuid.uuid4())).hexdigest()
					password_reset_key = salt + uid
					user.profile.password_reset_key = password_reset_key
					user.profile.save()
					mail_body = settings.HOST_BASE_URL + u'accounts/reset/?a=' + password_reset_key + '&z=' + user.profile.uuid
					send_mail_task.delay( mail_subject, mail_body, 'ghoshbinayak@gmail.com', [email])
					return render(request, 'accounts/forgot.html', {'success': 'Instructions have been sent to: ' + email})
				else:
					return render(request, 'accounts/forgot.html', {'error': 'Your account is not active.'})
			except robodarshanMember.DoesNotExist:
				return render(request, 'accounts/forgot.html', {'error': 'The email id is not registered.'})
	else:
		form = forms.ForgotForm()
		return render(request, 'accounts/forgot.html', {'form': form})

def reset(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('accounts:profile'))
	if request.method == 'POST':
		form = forms.ResetForm(request.POST)
		uid = request.POST.get('uid', False)
		password_reset_key = request.POST.get('password_reset_key', False)
		if form.is_valid() and uid and password_reset_key:
			new_password = form.cleaned_data.get('new_password')
			retype_password = form.cleaned_data.get('retype_password')			
			try:
				user = Profile.objects.get(uuid = uid).user
			except Profile.DoesNotExist:
				return render(request, 'accounts/reset.html', {'error': 'Sorry something went wrong.'})
			if user.profile.password_reset_key == 'NULL' or user.profile.password_reset_key != password_reset_key:
				return render(request, 'accounts/reset.html', {'error': 'Link expired.'})
			else:
				user.set_password(new_password)
				user.profile.password_reset_key = "NULL";
				user.save()
				return render(request, 'accounts/reset.html', {'success': 'Password reset successfully.'})
		else:
			return render(request, 'accounts/reset.html', {'error': 'Something went wrong.'})
	else:
		uid = request.GET.get('z', False)
		password_reset_key = request.GET.get('a', False)
		if uid and password_reset_key:	
			try:
				user = Profile.objects.get(uuid = uid).user
			except Profile.DoesNotExist:
				return render(request, 'accounts/reset.html', {'error': 'Sorry something went wrong. Ensure the link is correct.'})
			if user.profile.password_reset_key == 'NULL':
				return render(request, 'accounts/reset.html', {'error': 'Link expired.'})
			else:	
				if user.profile.password_reset_key == password_reset_key:
					form = forms.ResetForm()
					return render(request, 'accounts/reset.html', {'form': form, 'uid' : uid, 'password_reset_key': password_reset_key})
				else:
					return render(request, 'accounts/reset.html', {'success': 'Invalid key.'})
		else:
			return render(request, 'accounts/reset.html', {'error': 'Sorry something went wrong. Ensure the link is correct.'})
