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


class ProductType(models.Model):
    """Модель типа товара"""
    name = models.CharField(max_length=255, verbose_name='Название типа товара')
    slug = models.SlugField(unique=True, db_index=True)

    class Meta:
        db_table = 'ProductType'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=255, verbose_name='Название товара', db_index=True)
    slug = models.SlugField(unique=True, db_index=True, blank=True, null=True, default=None, max_length=255)
    author = models.CharField(max_length=255, verbose_name='ФИО автора')
    description = models.TextField(verbose_name='Описание товара')
    image = models.ImageField(upload_to='product_img/', verbose_name='Картинка товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField()
    rubric = models.ManyToManyField('ProductRubric', related_name='product')
    # Тип товара (Цифровой, или материальный). При создании автоматически будет присвоено значение. Может быть одновременно два типа
    type_of_product = models.ManyToManyField('ProductType', blank=True, default='type_of_product')
    # Файл продукции присваевается только цифровому типу товара
    file = models.FileField(upload_to='product_files/', verbose_name='Файл товара', blank=True, null=True)
    # Вес и кол-во товара на складе присваевается только материальному товару
    weight = models.PositiveIntegerField(verbose_name='Вес товара', blank=True, null=True)
    count_of_product = models.PositiveIntegerField(verbose_name='Кол-во товара на складе', blank=True, null=True)

    class Meta:
        db_table = 'Product'

    def save(self, *args, **kwargs):
        # Проверка типа товара и генерация slug
        try:
            if self.file and self.weight and self.count_of_product:
                self.slug = 'material-and-digital-' + slugify(self.name)
            elif self.file:
                self.slug = 'digital-' + slugify(self.name)
            elif self.weight and self.count_of_product:
                self.slug = 'material-' + slugify(self.name)
        except:
            return redirect('/admin/catalog/product/')
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}.'
