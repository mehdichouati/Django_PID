from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Artist, Show, Review, UserMeta


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


class RegisterForm(forms.Form):
    login = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    firstname = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    langue = forms.ChoiceField(
        choices=[('FR', 'Français'), ('EN', 'English'), ('NL', 'Nederlands')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(username=login).exists():
            raise ValidationError("Ce login est déjà utilisé.")
        return login

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data


class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ['location', 'slug', 'title', 'poster_url', 'duration', 'created_in', 'bookable']
        widgets = {
            'location': forms.Select(attrs={'class': 'form-select'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'poster_url': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'created_in': forms.NumberInput(attrs={'class': 'form-control'}),
            'bookable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'stars']
        widgets = {
            'review': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Votre avis sur ce spectacle...'
            }),
            'stars': forms.Select(
                choices=[(i, i) for i in range(1, 6)],
                attrs={'class': 'form-select'}
            ),
        }

    def clean_review(self):
        review = self.cleaned_data['review'].strip()
        if not review:
            raise forms.ValidationError("L'avis ne peut pas être vide.")
        return review


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=60, label="Prénom", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=60, label="Nom", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    langue = forms.ChoiceField(
        choices=[('FR', 'Français'), ('EN', 'English'), ('NL', 'Nederlands')],
        label="Langue",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)
        if qs.exists():
            raise ValidationError("Cet email est déjà utilisé par un autre compte.")
        return email