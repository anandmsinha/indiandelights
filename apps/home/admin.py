from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Cities, Vendors, Taste, UnitType, Categories, Item, HomePage


class UnitTypeForm(ModelForm):
    """
        Check that only one of the field is checked either weight or
        piece.
    """

    def clean(self):
        cleaned_data = super(UnitTypeForm, self).clean()
        weight = cleaned_data.get("weight")
        piece = cleaned_data.get("piece")
        if weight == piece:
            raise ValidationError('You can select only one of weight and piece.')


class UnitTypeAdmin(admin.ModelAdmin):
    form = UnitTypeForm


admin.site.register(Cities)
admin.site.register(Vendors)
admin.site.register(Taste)
admin.site.register(UnitType, UnitTypeAdmin)
admin.site.register(Item)
admin.site.register(Categories)
admin.site.register(HomePage)
