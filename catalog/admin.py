from django.contrib import admin
from django.shortcuts import redirect


from .models import Product, ProductRubric, ProductType


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'price', 'is_available', 'created', 'updated']
    list_filter = ['is_available', 'created', 'updated']
    list_editable = ['price', 'is_available']

    def save_related(self, request, form, formsets, change):
        digital = ProductType.objects.get(name="Цифровой товар")
        material = ProductType.objects.get(name="Материальный товар")
        try:
            if form.cleaned_data['file'] and form.cleaned_data['weight'] and form.cleaned_data['count_of_product']:
                form.cleaned_data['type_of_product'] = [digital, material]
            elif form.cleaned_data['file']:
                form.cleaned_data['type_of_product'] = [digital]
            elif form.cleaned_data['weight'] and form.cleaned_data['count_of_product']:
                form.cleaned_data['type_of_product'] = [material]
        except:
            return redirect('/admin/catalog/product/')
        form.save_m2m()
        for formset in formsets:
             self.save_formset(request, form, formset, change=change)



@admin.register(ProductRubric)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
