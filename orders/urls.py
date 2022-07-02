from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.OrderCreate.as_view(), name='order_create'),
    path('created/<int:pk>/', views.OrderCreated.as_view(), name='order_created'),

]