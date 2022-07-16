from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    """Форма оформления заказа"""
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'country', 'city', 'mail', 'email']
        labels = {
            'first_name': False,
            'last_name': False,
            'country': False,
            'city': False,
            'mail': False,
            'email': False,
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Имя'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Фамилия'
            }),

            'country': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Страна'
            }),

            'city': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Укажите город'
            }),

            'mail': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Отделение новой почты'
            }),

            'email': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Введите ваш Email'
            }),
        }
