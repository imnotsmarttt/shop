from .models import ProductRubric, ProductType


class HeaderContextMixin:
    """Миксин передающий контекст для шапки навигации"""
    def get_header_context(self, **kwargs):
        context = kwargs
        context['rubrics'] = ProductRubric.objects.all()
        context['types'] = ProductType.objects.all()
        return context