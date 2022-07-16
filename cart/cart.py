from decimal import Decimal

from django.conf import settings

from catalog.models import Product
from coupons.models import Coupon


class Cart(object):
    """Объект корзины"""
    def __init__(self, request):
        # Инициализация корзины
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, update_quantity=False):
        # Добавление товара в корзину, или обновление его количества
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Сохраняем сессию
        self.session.modified = True

    def remove(self, product):
        # Удаление товара из корзины
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            if self.coupon:
                item_price = round(Decimal(item['price']) - Decimal((self.coupon.discount / 100) * float(item['price'])), ndigits=2)
                item['price_without_discount'] = Decimal(item['price'])
            elif not self.coupon:
                item_price = Decimal(item['price'])
            item['price'] = item_price
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        # Цена всех товаров в корзине
        return sum(
            Decimal(item['price']) * item['quantity'] for item in self.cart.values()
        )

    def clear(self):
        # Очистка всей корзины
        del self.session[settings.CART_SESSION_ID]
        self.save()

    # Система купона
    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None
