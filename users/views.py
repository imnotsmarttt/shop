from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserRegisterForm, UserAuthenticateForm
from users.models import CustomUser
from orders.models import Order


class UserRegister(CreateView):
    """Регистрация пользователя"""
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = 'index'


class UserAuthenticate(LoginView):
    """Аутентификация пользователя"""
    form_class = UserAuthenticateForm
    template_name = 'users/login.html'
    success_url = 'index'


class UserLogout(LogoutView):
    """Выход пользователя"""
    template_name = 'users/logout.html'


class UserProfile(DetailView):
    """Профиль пользователя"""
    template_name = 'users/profile.html'
    model = CustomUser
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        # Получение заказов определенного пользователя
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.get_object()).order_by('-created')
        return context


