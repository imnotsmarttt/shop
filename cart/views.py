from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

from catalog.models import Product

from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponForm


class CartDetail(FormMixin, TemplateView):
    template_name = 'cart/cart_detail.html'
    form_class = CouponForm


def cart_add(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, id=pk)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'])
    return redirect('cart_detail')


def cart_del(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, id=pk)
    cart.remove(product)
    return redirect('cart_detail')

