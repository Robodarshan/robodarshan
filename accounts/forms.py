# appname/forms.py

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import becAlumnus
from django import forms as django_forms

class becAlumnusCreationForm(UserCreationForm):
	"""
	A form that creates a user, with no privileges, from the given email and
	password.
	"""

	def __init__(self, *args, **kargs):
		super(becAlumnusCreationForm, self).__init__(*args, **kargs)
		del self.fields['username']

	class Meta:
		model = becAlumnus
		fields = ("email", "fullname", "nickname",
				"date_of_birth", "batch_of", "department",
				"is_staff", "is_active")

class becAlumnusChangeForm(UserChangeForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""

	def __init__(self, *args, **kargs):
		super(becAlumnusChangeForm, self).__init__(*args, **kargs)
		del self.fields['username']

	class Meta:
		model = becAlumnus

class RegistrationForm(django_forms.Form):
	"""
	A form that used in the site's registration page
	to register new users.
	"""
	fullname = django_forms.CharField(max_length=200)
	email = django_forms.EmailField()
	password = django_forms.CharField(max_length=100, widget=django_forms.PasswordInput)
	retype_password = django_forms.CharField(max_length=100, widget=django_forms.PasswordInput)
	nickname = django_forms.CharField(max_length=50, required=False)
	date_of_birth = django_forms.DateField()
	batch_of = django_forms.DateField()
	department = django_forms.CharField(max_length=100)

	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		# check if email exists
		email = cleaned_data.get("email")
		try:
			becAlumnus.objects.get(email= email)
			try:
				self.errors['email'].append("email already exists.")
			except KeyError:
				self.errors['email'] = ["email already exists."]
		except becAlumnus.DoesNotExist:
			pass

		# check if the passwords match
		password = cleaned_data.get("password")
		retype_password = cleaned_data.get("retype_password")
		if password and retype_password and (password != retype_password):
			try:
				self.errors['retype_password'].append("passwords didn't match.")
			except KeyError:
				self.errors['retype_password'] = ["passwords didn't match."]
		return cleaned_data

class LoginForm(django_forms.Form):
	email = django_forms.EmailField()
	password = django_forms.CharField(max_length=100, widget=django_forms.PasswordInput)

class ForgotForm(django_forms.Form):
	email = django_forms.EmailField()

class ResetForm(django_forms.Form):	
	new_password = django_forms.CharField(max_length=100, widget=django_forms.PasswordInput)
	retype_password = django_forms.CharField(max_length=100, widget=django_forms.PasswordInput)
	def clean(self):
		cleaned_data = super(ResetForm, self).clean()
		# check if the passwords match
		password = cleaned_data.get("new_password")
		retype_password = cleaned_data.get("retype_password")
		if password and retype_password and (password != retype_password):
			try:
				self.errors['retype_password'].append("passwords didn't match.")
			except KeyError:
				self.errors['retype_password'] = ["passwords didn't match."]
		return cleaned_data