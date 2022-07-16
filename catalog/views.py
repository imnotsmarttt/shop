from decimal import Decimal

from django.shortcuts import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.contrib.postgres.search import SearchVector

from .models import Product

from cart.forms import CartAddProductForm
from comments.forms import CommentForm
from comments.models import ProductComment


def is_valid_queryset_param_list(param):
    return param != [] and param is not None


def is_valid_queryset_param_stroke(param):
    return param != '' and param is not None


class MainPage(ListView):
    template_name = 'catalog/main_page.html'
    model = Product


class ProductList(ListView):
    """Отображение продуктов"""
    model = Product
    template_name = 'catalog/product_list.html'
    paginate_by = 2

    def get_queryset(self):
        # queryset для поиска и фильтрации товара по разным полям
        qs = Product.objects.filter(is_available=True)
        type_query = self.request.GET.getlist('type')
        rubric_query = self.request.GET.getlist('rubric')
        min_price_query = self.request.GET.get('min_price')
        max_price_query = self.request.GET.get('max_price')
        search_query = self.request.GET.get('search')

        if is_valid_queryset_param_list(type_query):
            qs = qs.filter(type_of_product__slug__in=type_query)

        if is_valid_queryset_param_list(rubric_query):
            qs = qs.filter(rubric__slug__in=rubric_query)

        if is_valid_queryset_param_stroke(min_price_query):
            qs = qs.filter(price__gte=min_price_query)

        if is_valid_queryset_param_stroke(max_price_query):
            qs = qs.filter(price__lt=max_price_query)

        if is_valid_queryset_param_stroke(search_query):
            qs = qs.annotate(search=SearchVector('name', 'author')).filter(search=search_query)

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(*kwargs)
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
        # Форма публикации комментария
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
