from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField()

    class Meta:
        model = Profile
        fields = ('email', 'username', 'password1', 'password2')
