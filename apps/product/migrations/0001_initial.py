# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeImages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=b'config')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('leftMenu', models.BooleanField(default=True, help_text=b'True if item appears in left menu, in case of top menu set false.', verbose_name=b'Is left item')),
                ('label', models.CharField(max_length=100)),
                ('category', models.ForeignKey(to='home.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
