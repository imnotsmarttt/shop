from django.shortcuts import render
from django.views.generic import ListView

from .models import Product, ProductType

def index(request):
    return render(request, 'index.html')


class Catalog(ListView):
    model = Product
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(*kwargs)
        context['types'] = ProductType.objects.all()
        if self.kwargs:
            type = ProductType.objects.get(slug=self.kwargs['type_slug'])
            context['products'] = Product.objects.filter(type_of_product=type)
        else:
            context['products'] = Product.objects.all()
        return context