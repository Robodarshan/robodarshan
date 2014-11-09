# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='event',
            fields=[
                ('uuid', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('title', models.CharField(max_length=256)),
                ('cover_image_link', models.CharField(max_length=256)),
                ('time', models.DateTimeField()),
                ('location', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('announcements', models.TextField(default=b'NONE', blank=True)),
                ('coordinator1', models.ForeignKey(related_name='event_coordinator1', to=settings.AUTH_USER_MODEL)),
                ('coordinator2', models.ForeignKey(related_name='event_coordinator2', to=settings.AUTH_USER_MODEL)),
                ('volunteer1', models.ForeignKey(related_name='event_volunteer1', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('volunteer2', models.ForeignKey(related_name='event_volunteer2', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
