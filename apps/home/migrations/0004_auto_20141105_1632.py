# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_vendors'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('metadata', models.TextField(default=b'{}', blank=True)),
                ('categories', models.ManyToManyField(related_name='categories_rel_+', null=True, to='home.Categories', blank=True)),
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
                ('categories', models.ManyToManyField(to='home.Categories', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Taste',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TasteRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(default=0.5)),
                ('child', models.ForeignKey(related_name=b'+', to='home.Taste')),
                ('parent', models.ForeignKey(to='home.Taste')),
            ],
            options={
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
            field=models.ForeignKey(to='home.Vendors'),
            preserve_default=True,
        ),
    ]
