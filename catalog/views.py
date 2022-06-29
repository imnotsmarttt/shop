from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Product, ProductType, ProductRubric


class ProductList(ListView):
    model = Product
    template_name = 'catalog/product_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(*kwargs)
        context['rubrics'] = ProductRubric.objects.all()
        context['types'] = ProductType.objects.all()
        context['products'] = Product.objects.all()
        return context


class ProductListFilter(ListView):
    model = Product
    template_name = 'catalog/product_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(*kwargs)
        context['rubrics'] = ProductRubric.objects.all()
        context['types'] = ProductType.objects.all()
        context['products'] = Product.objects.filter(
            Q(type_of_product__slug__in=self.request.GET.getlist('type')) |
            Q(rubric__slug__in=self.request.GET.getlist('rubric'))
        ).distinct()
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

