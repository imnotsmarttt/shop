from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Product

from cart.forms import CartAddProductForm


class MainPage(ListView):
    template_name = 'catalog/main_page.html'
    model = Product


class ProductList(ListView):
    """Отображение продуктов"""
    model = Product
    template_name = 'catalog/product_list.html'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(*kwargs)
        context['products'] = Product.objects.filter(is_available=True)
        context['max_price'] = self.get_queryset().order_by('-price').first()
        context['min_price'] = self.get_queryset().order_by('price').first()
        return context


class ProductListFilter(ListView):
    """Отображение отфильтрованных продуктов"""
    model = Product
    template_name = 'catalog/product_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.filter(
            Q(type_of_product__slug__in=self.request.GET.getlist('type')) |
            Q(rubric__slug__in=self.request.GET.getlist('rubric')) |
            Q(price__range=(self.request.GET.get('min_price'), self.request.GET.get('max_price')))
        ).distinct()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['max_price'] = self.get_queryset().order_by('-price').first()
        context['min_price'] = self.get_queryset().order_by('price').first()
        return context


class ProductDetail(DetailView):
    """Отображение детальной информации конкретного продукта"""
    model = Product
    template_name = 'catalog/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CartAddProductForm
        return context

