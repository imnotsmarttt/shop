import datetime

from django import forms

from .models import Coupon


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code']
        labels = {
            'code': ''
        }

        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Купон на скидку'
            })
        }

