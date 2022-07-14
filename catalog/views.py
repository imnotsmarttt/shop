from django.shortcuts import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.db.models import Q

from .models import Product

from cart.forms import CartAddProductForm
from comments.forms import CommentForm
from comments.models import ProductComment


class MainPage(ListView):
    template_name = 'catalog/main_page.html'
    model = Product


class ProductList(ListView):
    """Отображение продуктов"""
    model = Product
    template_name = 'catalog/product_list.html'
    paginate_by = 2

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
    paginate_by = 2

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


class ProductDetail(DetailView, FormMixin):
    """Отображение детальной информации конкретного продукта"""
    model = Product
    template_name = 'catalog/product_detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_add_to_cart'] = CartAddProductForm
        context['comments'] = ProductComment.objects.filter(product=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.user = self.request.user
            comment.product = self.get_object()
            comment.save()
            return super(ProductDetail, self).form_valid(form)
        else:
            form.add_error('__all__', 'Комментарий могут оставлять только аутентифицированные пользователи))')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('product_detail', kwargs={'slug': self.get_object().slug})
