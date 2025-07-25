from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class RegisterForm(UserCreationForm):
    class Meta():
        model = get_user_model()
        fields = ["email", "first_name", "last_name", "password1", "password2"]


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()
