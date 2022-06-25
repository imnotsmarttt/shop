from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.template.defaultfilters import slugify as django_slugify

from users.models import CustomUser

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def slugify(s):
    """Транскрипция русского слага"""
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


class ProductCategory(models.Model):
    """Категория товаров"""
    name = models.CharField(max_length=255, verbose_name='Категория товара')
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductCategory, self).save(*args, **kwargs)


class Product(models.Model):
    """Модель продукта"""
    name = models.CharField(max_length=255, verbose_name='Название товара')
    author = models.CharField(max_length=255, verbose_name='ФИО автора')
    description = models.TextField(verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')
    # Тип продукта(Цифровой и физичесский), при создании будет автоматически присвоено значение
    type_of_product = models.CharField(max_length=255, verbose_name='Тип товара', blank=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    is_available = models.BooleanField()
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, related_name='product')

    class Meta:
        db_table = 'Product'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name


class DigitalProduct(Product):
    """Модель Цифровой продукта"""
    file = models.FileField()

    def save(self, *args, **kwargs):
        self.type_of_product = 'Цифровой'
        self.slug = 'digital-' + slugify(self.name)
        super(DigitalProduct, self).save(*args, **kwargs)

    class Meta:
        db_table = 'DigitalProduct'


class MaterialProduct(Product):
    """Модель физического продукта"""
    weight = models.PositiveIntegerField(verbose_name='Вес товара')
    count_of_product = models.PositiveIntegerField(verbose_name='Кол-во товаров на складе')

    def save(self, *args, **kwargs):
        self.type_of_product = 'Физический'
        self.slug = 'material-' + slugify(self.name)
        super(MaterialProduct, self).save(*args, **kwargs)

    class Meta:
        db_table = 'MaterialProduct'


class ProductReview(MPTTModel):
    """MPTT модель отзывов товара"""
    content = models.TextField(verbose_name='Отзыв')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='product_review')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='review')
    created = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey(CustomUser, on_delete=models.CASCADE, related_name='review_children', blank=True, null=True)

    class Meta:
        db_table = 'ProductReview'
