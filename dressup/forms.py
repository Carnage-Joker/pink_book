# dressup/forms.py

from django import forms
from .models import Avatar


class AvatarCreationForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['skin', 'body']  # Only include skin and body fields
        widgets = {
            'skin': forms.RadioSelect(),
            'body': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(AvatarCreationForm, self).__init__(*args, **kwargs)
        # Filter body choices to include only '00' and '01'
        self.fields['body'].choices = [
            (value, label) for value, label in self.fields['body'].choices if value in ['00', '01']
        ]
