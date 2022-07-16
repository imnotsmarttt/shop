from django.shortcuts import reverse
from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

from catalog.models import Product
from users.models import CustomUser


class ProductComment(MPTTModel):
    """Древовидная модель комментариев к продукту"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='product_comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(verbose_name='Комментарий к продукту')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ProductComment'

    class MPTTMeta:
        order_insertion_by = '-created'

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.product.slug})
