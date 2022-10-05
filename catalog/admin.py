from django.contrib import admin

from .models import Product, ProductRubric

# Автозаполнение продукции
# from .util.auto_fill_product import auto_fill


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'price', 'is_available', 'created', 'updated']
    list_filter = ['is_available', 'created', 'updated']
    list_editable = ['price', 'is_available']


@admin.register(ProductRubric)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
