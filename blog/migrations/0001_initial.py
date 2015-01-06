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
            name='story',
            fields=[
                ('uuid', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('subtitle', models.TextField()),
                ('body', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('permalink', models.CharField(max_length=256)),
                ('published', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
