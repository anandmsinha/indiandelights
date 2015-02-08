from django.forms import ModelForm, widgets
from .models import Applicants


class ApplicantsForm(ModelForm):

    class Meta:
        model = Applicants
        fields = ['email', 'name', 'phone', 'business']
        widgets = {
            'email': widgets.EmailInput(
                attrs={
                    'placeholder': 'Email adress',
                    'required': 'true'
                },
            ),
            'name': widgets.TextInput(
                attrs={
                    'placeholder': 'Full name',
                    'required': 'true'
                },
            ),
            'phone': widgets.TextInput(
                attrs={
                    'placeholder': 'Contact number',
                    'required': 'true'
                },
            ),
            'business': widgets.TextInput(
                attrs={
                    'placeholder': 'Type of business',
                    'required': 'true'
                },
            ),
        }
