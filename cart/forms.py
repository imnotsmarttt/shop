from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """Форма добавления товара в корзину"""
    # quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label=False)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, product, *args, **kwargs):
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        qs = product.count_of_product
        self.fields['quantity'] = forms.TypedChoiceField(choices=[(o, str(o)) for o in range(qs+1)], coerce=int, label=False)
