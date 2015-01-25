# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_homepage_is_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendors',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vendors',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to=b'config', blank=True),
            preserve_default=True,
        ),
    ]
