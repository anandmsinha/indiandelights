from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.conf import settings
from datetime import date
from os.path import join
from uuid import uuid4

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField

import json


class AppUserManager(BaseUserManager):

    """
    Main manager class since we are using email based authentication.
    """

    def _create_user(self, email, password, is_staff, is_superuser,
                     **extra_fields):
        if not email:
            raise ValueError('Email field is required for every user.')
        email = self.normalize_email(email)
        is_active = extra_fields.pop('is_active', True)
        user = self.model(email=email, is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        is_staff = extra_fields.pop('is_staff', False)
        return self._create_user(email=email, password=password,
                                 is_staff=is_staff, is_superuser=False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email=email, password=password, is_staff=True,
                                 is_superuser=True, **extra_fields)


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email adress', max_length=255, unique=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    time_joined = models.DateTimeField(auto_now_add=True)

    objects = AppUserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_username(self):
        return self.email

    def get_short_name(self):
        return self.email


class Cities(models.Model):

    """
    Class for cities
    """

    name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name


class Vendors(models.Model):

    """
    Class for handling vendors.
    """

    name = models.CharField(max_length=100)
    city = models.ForeignKey(Cities)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    delivers_in = models.ManyToManyField(
        Cities, blank=True, null=True, related_name='delivers')
    image = ProcessedImageField(upload_to='config',
        processors=[ResizeToFill(160, 100)], format='JPEG', options={'quality': 80}, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_delivery_cities(self):
        delivery_cities = [city.name for city in self.delivers_in.all()]
        return ', '.join(delivery_cities)


class Taste(models.Model):

    """
    class for representing taste of items.
    """

    type = models.CharField(max_length=200)

    def __unicode__(self):
        return self.type


class UnitType(models.Model):

    """
    Class for representing diffrent unit types like 1Kg, 1/2 Kg
    """

    display_name = models.CharField(max_length=200)
    weight = models.BooleanField(default=True)
    piece = models.BooleanField(default=False)

    def __unicode__(self):
        return self.display_name


class Categories(models.Model):

    """
    Class for category of product like diwali sale, sweet, salty
    """

    name = models.CharField(max_length=100)
    metadata = models.TextField(default='{}', blank=True)

    def __unicode__(self):
        return self.name


# function to generate name of folder where image will be stored.


def image_upload_rename(self, filename):
    path = 'items'
    ext = filename.split('.')[-1]
    if self.pk:
        filename = '{}.{}'.format(self.pk, ext)
    else:
        today_date = date.today()
        filename = '{}{}{}{}.{}'.format(str(today_date.year), str(today_date.month), str(today_date.day), uuid4().hex,ext)
    return join(path, filename)


class Item(models.Model):

    """
    Class for representing a single item that is product.
    """

    name = models.CharField(max_length=200)
    vendor = models.ForeignKey(Vendors)
    available = models.BooleanField(default=True)
    taste = models.ForeignKey(Taste)
    unit = models.ForeignKey(UnitType)
    made_with = models.TextField(null=True, blank=True)
    price = models.FloatField(default=100.0)
    categories = models.ManyToManyField(
        Categories, blank=True, null=True)
    image = models.ImageField(upload_to=image_upload_rename)
    image_thumbnail = ImageSpecField(source='image', processors=[
                                     ResizeToFill(260, 208)], format='JPEG',
                                     options={'quality': 80})
    image_lg_thumbnail = ImageSpecField(source='image', processors=[
                                        ResizeToFill(450, 450)], format='JPEG',
                                        options={'quality': 80})
    image_small_thumbnail = ImageSpecField(source='image', processors=[
        ResizeToFill(40, 36)], format='JPEG', options={'quality': 80})

    def __unicode__(self):
        return self.name

    def get_availability_message(self):
        text_class = 'text-danger'
        text_message = 'Out of stock'
        if self.available:
            text_class = 'text-success'
            text_message = 'In stock'
        return '<span class="{0}">{1}</span>'.format(text_class, text_message)


class HomePage(models.Model):

    """
    Model for representing item which will be shown on home page.
    """

    category = models.ForeignKey(Categories, blank=False, null=False)
    metadata = models.TextField(default='{}', blank=True)
    order = models.PositiveIntegerField(null=True, blank=True)
    is_config = models.BooleanField(default=False)

    metacache = None
    is_decoded = False
    main_items = []

    def __unicode__(self):
        if self.category:
            return unicode(self.category)
        return 'HomeCat'

    def decode_json(self):
        if not self.is_decoded:
            self.is_decoded = True
            try:
                self.metacache = json.loads(self.metadata)
            except Exception, e:
                self.metacache = {}

    def get_page_limit(self):
        if 'grids' in self.metacache:
            tmp_val = int(self.metacache['grids'])
            if tmp_val > 0:
                return tmp_val
        return 6

    def get_label(self):
        if 'label' in self.metacache:
            return self.metacache['label']
        return self.category.name

    def fetch_items(self):
        self.main_items = Item.objects.filter(
            categories__pk__exact=self.category.pk).select_related('unit')[:self.get_page_limit()]
