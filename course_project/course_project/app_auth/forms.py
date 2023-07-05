from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ('email', 'password1', 'password2')
