# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_cities'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('city', models.ForeignKey(to='home.Cities')),
                ('delivers_in', models.ManyToManyField(related_name=b'delivers', null=True, to='home.Cities', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
