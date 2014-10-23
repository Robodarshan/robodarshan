import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.dispatch import Signal, receiver


from accounts.tasks import send_mail_task

# signal sent when user is created
user_created = Signal(providing_args=["email"])

# Custom User Manager for robodarshan website


class robodarshanMemberManager(BaseUserManager):

    """user manager for robodarshanMember"""

    def _create_user(self,
                     email,
                     password,
                     is_staff,
                     is_superuser,
                     **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # send signal to the profile creater
        user_created.send(sender=self, email=email)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email,
                                 password,
                                 True,
                                 True,
                                 is_active=True,
                                 **extra_fields)


# Custom User Model for robodarshan website

class robodarshanMember(AbstractBaseUser, PermissionsMixin):

    """custor user model for Robodarshan website"""
    email = models.EmailField(max_length=254, unique=True)
    fullname = models.CharField(max_length=200)
    is_staff = models.BooleanField(_('staff status'),
                                   default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'),
                                    default=False,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    # NOTE: date_joined is the day the user account is created, not the date
    # of joining the institute.
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = robodarshanMemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['fullname']

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        if self.fullname:
            return self.fullname
        else:
            return "mask man"

    def get_short_name(self):
        "Returns the nickname for the user."
        if self.fullname:
            return str(self.fullname).split()[0]
        else:
            return "maskman"

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail_task.delay(subject, message, from_email, [self.email])

# User profile


class Profile(models.Model):
    batch_of = models.CharField(max_length=4, blank=True)
    department = models.CharField(max_length=100, blank=True)
    email_verify_key = models.CharField(max_length=100, blank=True)
    password_reset_key = models.CharField(max_length=100, blank=True)
    password_reset_key_timestamp = models.DateTimeField(blank=True, null=True)
    uuid = models.CharField(max_length=100, blank=True)
    facebook_link = models.CharField(max_length=254, blank=True)
    phone = models.CharField(max_length=20)
    is_private = models.BooleanField(default=False)
    user = models.OneToOneField(robodarshanMember)

    def __unicode__(self):
        return self.user.email

# create profile when new user is created


@receiver(user_created)
def create_profile(sender, **kwargs):
    user = robodarshanMember.objects.get(email=kwargs.get('email'))
    profile = Profile(user=user)
    profile.uuid = str(uuid.uuid1())
    profile.save()
