from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserRegisterForm, UserAuthenticateForm


class UserRegister(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = 'index'


class UserAuthenticate(LoginView):
    form_class = UserAuthenticateForm
    template_name = 'users/login.html'
    success_url = 'index'


class UserLogout(LogoutView):
    template_name = 'users/logout.html'
