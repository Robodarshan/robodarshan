from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_mail_task(subject, message, from_email, to_email):
    send_mail(subject, message, from_email, to_email)


@shared_task
def delete_email_task(uuid):
    from accounts.models import Profile
    try:
        user = Profile.objects.get(uuid=uuid).user
    except Profile.DoesNotExist:
        return False
    user.delete()
