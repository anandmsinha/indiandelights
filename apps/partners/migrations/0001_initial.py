# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicants',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'email adress')),
                ('name', models.CharField(max_length=100, verbose_name=b'Full name')),
                ('phone', models.CharField(help_text=b'No need to write country code. In case of mobile just number and in case of landline stdcode and phone number. example 805012xxxx and for landline 03595 259506', max_length=12, verbose_name=b'Phone number', validators=[django.core.validators.RegexValidator(regex=b'((\\+*)((0[ -]+)*|(91 )*)(\\d{12}|\\d{10}))|\\d{5}([- ]*)\\d{6}', message=b'Invalid phone number')])),
                ('business', models.CharField(max_length=100, verbose_name=b'Type of business')),
                ('processed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
