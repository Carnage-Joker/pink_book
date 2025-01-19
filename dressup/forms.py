from django import forms
from .models import Avatar


class AvatarCreationForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['skin', 'body']
        widgets = {
            'skin': forms.RadioSelect(),
            'body': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skin'].widget.attrs.update({'class': 'skin-selection'})
        self.fields['body'].widget.attrs.update({'class': 'body-selection'})
