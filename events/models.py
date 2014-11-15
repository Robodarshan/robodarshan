from django.db import models
from accounts.models import robodarshanMember


class event(models.Model):

    """an event instance"""
    uuid = models.CharField(max_length=32, primary_key=True)
    timestamp = models.DateTimeField()  # will be added automatically
    title = models.CharField(max_length=256)
    cover_image_link = models.CharField(max_length=256)
    time = models.DateTimeField()
    location = models.CharField(max_length=256)
    description = models.TextField()
    coordinator1 = models.ForeignKey(
        robodarshanMember, related_name='event_coordinator1')
    coordinator2 = models.ForeignKey(
        robodarshanMember, related_name='event_coordinator2')
    volunteer1 = models.ForeignKey(
        robodarshanMember, blank=True,
        null=True, related_name='event_volunteer1')
    volunteer2 = models.ForeignKey(
        robodarshanMember, blank=True,
        null=True, related_name='event_volunteer2')
    announcements = models.TextField(default="NONE", blank=True)

    def __unicode__(self):
        return self.title


class event_list(models.Model):

    """approved_event stores the list of events currently displayed"""
    f_uuid = models.CharField(max_length=32, primary_key=True)  # uuid of first instance
    # uuid of current event instance
    c_uuid = models.ForeignKey(event, related_name='approved_event_current')
    # uuid of latest event instance
    l_uuid = models.ForeignKey(event, related_name='approved_event_latest')
    published = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)  # time last updated
