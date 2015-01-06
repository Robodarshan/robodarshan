from django.db import models
from accounts.models import robodarshanMember


class story(models.Model):
    uuid = models.CharField(max_length=32, primary_key=True)
    title = models.CharField(max_length=256)
    body = models.TextField()
    timestamp = models.DateTimeField()
    author = models.ForeignKey(robodarshanMember)
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title
