# dressup/forms.py

from django import forms
from .models import Avatar


class AvatarCreationForm(forms.ModelForm):
    class Meta:
        model = Avatar
        # Only include skin and body fields for creation
        fields = ['skin', 'body']
        widgets = {
            'skin': forms.RadioSelect(),
            'body': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(AvatarCreationForm, self).__init__(*args, **kwargs)
        # Optionally, filter body choices if needed
