from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"placeholder": "Tu usuario", "autofocus": True}),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"placeholder": "Tu contraseña"}),
    )

    error_messages = {
        "invalid_login": "Usuario o contraseña incorrectos.",
        "inactive": "Esta cuenta está desactivada.",
    }


class RegistroForm(UserCreationForm):
    email = forms.EmailField(label="Correo electrónico", required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")