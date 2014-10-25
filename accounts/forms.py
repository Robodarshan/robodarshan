# appname/forms.py

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import robodarshanMember
from django import forms as django_forms
from django.forms.widgets import Select


class robodarshanMemberCreationForm(UserCreationForm):

    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(robodarshanMemberCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = robodarshanMember
        fields = ("email", "fullname", "is_staff", "is_active")


class robodarshanMemberChangeForm(UserChangeForm):

    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(robodarshanMemberChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = robodarshanMember
        fields = '__all__'


class RegistrationForm(django_forms.Form):

    """
    A form that used in the site's registration page
    to register new users.
    """
    fullname = django_forms.CharField(max_length=200)
    email = django_forms.EmailField()
    password = django_forms.CharField(
        max_length=100, widget=django_forms.PasswordInput)
    retype_password = django_forms.CharField(
        max_length=100, widget=django_forms.PasswordInput)


class LoginForm(django_forms.Form):
    email = django_forms.EmailField()
    password = django_forms.CharField(
        max_length=100, widget=django_forms.PasswordInput)


class ForgotForm(django_forms.Form):
    email = django_forms.EmailField()


class ResetForm(django_forms.Form):
    new_password = django_forms.CharField(
        max_length=100, widget=django_forms.PasswordInput)
    retype_password = django_forms.CharField(
        max_length=100, widget=django_forms.PasswordInput)


DEPT_CHOICES = (('Information Technology', 'Information Technology',),
                ('Computer Science', 'Computer Science',),
                ('Aerospace', 'Aerospace',),
                ('Electronics', 'Electronics',),
                ('Mechanical', 'Mechanical',),
                ('Electrical', 'Electrical',),
                ('Metalurgy', 'Metalurgy',),
                ('Mining', 'Mining',),
                ('Civil', 'Civil'),
                ('Architecture', 'Architecture')
                )

BATCH_CHOICES = [('2000', '2000'), ('2001', '2001'), ('2002', '2002'),
                 ('2003', '2003'), ('2004', '2004'), ('2005', '2005'),
                 ('2006', '2006'), ('2007', '2007'), ('2008', '2008'),
                 ('2009', '2009'), ('2010', '2010'), ('2011', '2011'),
                 ('2012', '2012'), ('2013', '2013'), ('2014', '2014'),
                 ('2015', '2015'), ('2016', '2016'), ('2017', '2017'),
                 ('2018', '2018')]


class ProfileEditForm(django_forms.Form):
    phone = django_forms.CharField(max_length=10, required=False)
    facebook = django_forms.CharField(max_length=100, required=False)
    department = django_forms.ChoiceField(
        required=False, widget=Select, choices=DEPT_CHOICES)
    batch_of = django_forms.ChoiceField(choices=BATCH_CHOICES, required=False)
