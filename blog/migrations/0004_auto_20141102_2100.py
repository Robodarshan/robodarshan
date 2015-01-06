# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_story_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='permalink',
        ),
        migrations.RemoveField(
            model_name='story',
            name='subtitle',
        ),
    ]
