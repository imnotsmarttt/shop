from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password', 'class': 'form-input', 'placeholder': 'Введите пароль'
        })
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password', 'class': 'form-input', 'placeholder': 'Повторите пароль'
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
        labels = {label: '' for label in fields}
        help_texts = {ht: '' for ht in fields}

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Введите логин'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Введите email'
            }),
        }


class UserAuthenticateForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'autofocus': True, 'class': 'form-input', 'placeholder': 'Введите логин'}))
    password = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password', 'class': 'form-input', 'placeholder': 'Введите пароль'}),
    )