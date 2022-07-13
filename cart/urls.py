from django.urls import path

from . import views

urlpatterns = [
    path('', views.CartDetail.as_view(), name='cart_detail'),
    path('<int:pk>/add/', views.cart_add, name='cart_add'),
    path('<int:pk>/del/', views.cart_del, name='cart_del'),
]