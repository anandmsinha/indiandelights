from django.db import models
from django.core.validators import RegexValidator


class Applicants(models.Model):

    email = models.EmailField('email adress', max_length=255, unique=True)
    name = models.CharField('Full name', max_length=100)
    phone = models.CharField('Phone number', max_length=12, validators=[
        RegexValidator(
            regex='((\+*)((0[ -]+)*|(91 )*)(\d{12}|\d{10}))|\d{5}([- ]*)\d{6}',
            message='Invalid phone number'
        )
    ], help_text='No need to write country code. In case of mobile just number and in case of landline stdcode and phone number. example 805012xxxx and for landline 03595 259506')
    business = models.CharField('Type of business', max_length=100)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
