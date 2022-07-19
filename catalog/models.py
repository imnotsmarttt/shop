from django.db import models
from django.template.defaultfilters import slugify as django_slugify
from django.shortcuts import redirect


alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def slugify(s):
    """Транскрипция slug с кириллицы на англ алфавит"""
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


class ProductRubric(models.Model):
    """Модель рубрики"""
    name = models.CharField(max_length=255, verbose_name='Название рубрики')
    slug = models.SlugField(unique=True, db_index=True)

    class Meta:
        db_table = 'ProductRubric'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Автоматическая генерация слага
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=255, verbose_name='Название товара', db_index=True)
    slug = models.SlugField(unique=True, db_index=True, blank=True, null=True, default=None, max_length=255)
    author = models.CharField(max_length=255, verbose_name='ФИО автора')
    description = models.TextField(verbose_name='Описание товара')
    image = models.ImageField(upload_to='product_img/', verbose_name='Картинка товара', default='product_img/prdct_img.jpg')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField()
    rubric = models.ManyToManyField('ProductRubric', related_name='product')
    weight = models.PositiveIntegerField(verbose_name='Вес товара', blank=True, null=True)
    count_of_product = models.PositiveIntegerField(verbose_name='Кол-во товара на складе', blank=True, null=True)

    class Meta:
        db_table = 'Product'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}.'
