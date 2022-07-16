from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserAuthenticate.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('profile/<slug:slug>/', views.UserProfile.as_view(), name='profile')
]