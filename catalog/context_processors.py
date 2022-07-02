from .models import ProductType, ProductRubric


def header_context(request):
    return {
        'rubrics': ProductRubric.objects.all(),
        'types': ProductType.objects.all()
    }