from django import forms
from .models import HelipadOwner


class HelipadOwnerForm(forms.ModelForm):
    class Meta:
        model = HelipadOwner
        fields = ['organization', 'country', 'city', 'address', 'phone', 'contact_name']
