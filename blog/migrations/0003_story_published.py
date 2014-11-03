# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_story_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='published',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
