from django.shortcuts import render, get_object_or_404, redirect

from catalog.models import Product

from .cart import Cart
from .forms import CartAddProductForm


def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


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

