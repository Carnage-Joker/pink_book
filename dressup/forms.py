from django import forms
from .models import Avatar


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['body_type', 'skin_tone', 'hair_type',
                  'hair_color']
        widgets = {
            'body_type': forms.Select(attrs={'class': 'form-control'}),
            'skin_tone': forms.Select(attrs={'class': 'form-control'}),
            'hair_type': forms.Select(attrs={'class': 'form-control'}),
            'hair_color': forms.Select(attrs={'class': 'form-control'}),
        }


class PremiumOutfitForm(forms.ModelForm):
    class Meta:
        model = PremiumOutfit
        fields = ['name', 'image', 'description', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class':
                                                     'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Form for adding a new favorite


class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorites
        fields = ['outfit']
        widgets = {
            'outfit': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FavoriteForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['outfit'].queryset = PremiumOutfit.objects.filter(
                user=user
            )
