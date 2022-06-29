from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Product, ProductType, ProductRubric
from .utils import HeaderContextMixin


class ProductList(HeaderContextMixin, ListView):
    """Отображение продуктов"""
    model = Product
    template_name = 'catalog/product_list.html'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(*kwargs)
        context['products'] = Product.objects.filter(is_available=True)
        context.update(self.get_header_context())
        return context


class ProductListFilter(HeaderContextMixin, ListView):
    """Отображение отфильтрованных продуктов"""
    model = Product
    template_name = 'catalog/product_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.filter(
            Q(type_of_product__slug__in=self.request.GET.getlist('type')) |
            Q(rubric__slug__in=self.request.GET.getlist('rubric'))
        ).distinct()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(*kwargs)
        context.update(self.get_header_context())
        return context


class ProductDetail(HeaderContextMixin, DetailView):
    """Отображение детальной информации конкретного продукта"""
    model = Product
    template_name = 'catalog/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_header_context())
        return context

