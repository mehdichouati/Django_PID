from django import forms
from .models import Artist


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['firstname', 'lastname']
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_firstname(self):
        firstname = self.cleaned_data['firstname'].strip()
        if not firstname:
            raise forms.ValidationError("Le prénom est obligatoire.")
        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data['lastname'].strip()
        if not lastname:
            raise forms.ValidationError("Le nom est obligatoire.")
        return lastname