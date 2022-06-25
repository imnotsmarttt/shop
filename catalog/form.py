from django import forms

from .models import Product, ProductType


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'author', 'description', 'image', 'price', 'is_available',
                  'rubric', 'file', 'weight', 'count_of_product']



