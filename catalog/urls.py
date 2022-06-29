from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('catalog/', views.ProductList.as_view(), name='catalog'),
    path('filter/<str:type_slug>', views.ProductList.as_view(), name='catalog_by_type'),
    path('filter/', views.ProductListFilter.as_view(), name='catalog_filter'),

    path('<str:slug>', views.ProductDetail.as_view(), name='product_detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)