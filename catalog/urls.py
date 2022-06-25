from django.urls import path

from . import views

urlpatterns = [
    path('', views.Catalog.as_view(), name='catalog'),
    path('<str:type_slug>', views.Catalog.as_view(), name='catalog_by_type'),
]