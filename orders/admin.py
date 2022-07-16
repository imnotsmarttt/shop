import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse

from .models import Order, OrderItem


def order_to_csv(modeladmin, request, queryset):
    """Генерация заказов в CSV"""
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' \
                                      'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many \
              and not field.one_to_many]
    # Заголовки полей
    writer.writerow([field.verbose_name for field in fields])
    # Запись данных
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


order_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['item']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'country', 'city', 'mail', 'paid', 'created']
    list_filter = ['paid', 'created']
    inlines = [OrderItemInline]
    actions = [order_to_csv]


