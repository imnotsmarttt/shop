from django.db import models

from catalog.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    country = models.CharField(max_length=255, verbose_name='Страна')
    city = models.CharField(max_length=255, verbose_name='Город')
    mail = models.CharField(max_length=255, verbose_name='Отделение Новой Почты')
    email = models.EmailField(verbose_name='Почта')
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False, verbose_name='Оплачено')

    class Meta:
        db_table = 'Order'

    def __str__(self):
        return f'Заказ № {self.id}'

    def get_total_price(self):
        return sum(item.get_cost() for item in self.order_item.all)


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_item')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кол-во')

    class Meta:
        db_table = 'OrderItem'

    def __str__(self):
        return f'{self.order}, {self.item}'

    def get_cost(self):
        return self.quantity * self.price
