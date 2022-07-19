from .models import ProductRubric


def header_context(request):
    """Контекст рубрики и типа для фильтрации товара в nav, в пункте - категории"""
    return {
        'rubrics': ProductRubric.objects.all(),
    }