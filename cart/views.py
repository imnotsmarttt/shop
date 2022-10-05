from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

from catalog.models import Product

from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponForm


class CartDetail(FormMixin, TemplateView):
    """Детальная информация о карзине"""
    template_name = 'cart/cart_detail.html'
    form_class = CouponForm


def cart_add(request, pk):
    """Добавление товара в корзину"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=pk)
    cart.add(product=product,
             quantity=int(request.POST.get('quantity')))
    return redirect('cart_detail')


def cart_del(request, pk):
    """Удаление товара из корзины"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=pk)
    cart.remove(product)
    return redirect('cart_detail')

