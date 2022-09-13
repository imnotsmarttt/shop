from django.urls import path

from . import views

urlpatterns = [
    path('post/', views.comment_post, name='comment_post')
]