# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import apps.home.models
import django.utils.timezone
import imagekit.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'email adress')),
                ('is_staff', models.BooleanField(default=False, verbose_name=b'staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name=b'active')),
                ('time_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name=b'children', blank=True, to='home.Category', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('metadata', models.TextField(default=b'{}', blank=True)),
                ('order', models.PositiveIntegerField(null=True, blank=True)),
                ('is_config', models.BooleanField(default=False)),
                ('category', models.ForeignKey(to='home.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('available', models.BooleanField(default=True)),
                ('made_with', models.TextField(null=True, blank=True)),
                ('price', models.FloatField(default=100.0)),
                ('image', models.ImageField(upload_to=apps.home.models.image_upload_rename)),
                ('category', models.ForeignKey(to='home.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Taste',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name=b'children', blank=True, to='home.Taste', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnitType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(max_length=200)),
                ('weight', models.BooleanField(default=True)),
                ('piece', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('image', imagekit.models.fields.ProcessedImageField(null=True, upload_to=b'config', blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('city', models.ForeignKey(to='home.City')),
                ('delivers_in', models.ManyToManyField(related_name=b'delivers', null=True, to='home.City', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='item',
            name='taste',
            field=models.ForeignKey(to='home.Taste'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.ForeignKey(to='home.UnitType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='vendor',
            field=models.ForeignKey(to='home.Vendor'),
            preserve_default=True,
        ),
    ]
