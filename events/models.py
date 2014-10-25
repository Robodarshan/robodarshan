from django.db import models
from accounts.models import robodarshanMember


class event(models.Model):
    timestamp = models.DateTimeField()  # will be added automatically
    title = models.CharField(max_length=256)
    cover_image_link = models.CharField(max_length=256)
    time = models.DateTimeField()
    location = models.CharField(max_length=256)
    description = models.TextField()
    coordinator1 = models.ForeignKey(robodarshanMember, related_name='+')
    coordinator2 = models.ForeignKey(robodarshanMember, related_name='+')
