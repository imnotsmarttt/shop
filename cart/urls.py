from django.urls import path

from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('<int:pk>/add/', views.cart_add, name='cart_add'),
    path('<int:pk>/del/', views.cart_del, name='cart_del'),
]