# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20141105_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('metadata', models.TextField(default=b'{}', blank=True)),
                ('order', models.PositiveIntegerField(null=True, blank=True)),
                ('category', models.ForeignKey(blank=True, to='home.Categories', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
