from django import forms
from . import models


# Simple Form for creating vehicle
class AddRentalForm(forms.ModelForm):
    class Meta:
        model = models.Vehicles_table

        fields = '__all__'
        exclude = ['is_rented', 'owner', 'currently_rented_by', 'rent_start']
