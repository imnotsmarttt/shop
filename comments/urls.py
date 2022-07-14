from django.urls import path

from . import views

urlpatterns = [
    path('reply/<int:parent_id>/<int:product_id>/', views.reply_comment, name='comment_reply')
]