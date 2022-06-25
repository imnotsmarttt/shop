from django.contrib import admin

from .models import ProductCategory, MaterialProduct, DigitalProduct


@admin.register(MaterialProduct)
class MaterialProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'price', 'is_available', 'created', 'count_of_product']


@admin.register(DigitalProduct)
class DigitalProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'price', 'is_available', 'created']


@admin.register(ProductCategory)
class DigitalProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
