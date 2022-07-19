import random
import os

from catalog.models import Product, ProductRubric


def auto_fill():
    x = len(Product.objects.all()) + 1
    for _ in range(1, 1100):

        rubric = ProductRubric.objects.order_by('?').first()
        name = f'Продукт: {rubric.name} - {x}.'
        author = f'Автор {x}'
        description = 'Описание'
        price = random.randint(99, 999)
        count_of_product = random.randint(1, 30)


        product = Product.objects.create(
            name=name,
            author=author,
            description=description,
            price=price,
            count_of_product=count_of_product,
            weight=1,
            is_available=True,
        )
        product.rubric.add(rubric)
        product.save()
        x += 1


auto_fill()