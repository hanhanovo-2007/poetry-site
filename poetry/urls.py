from django.urls import path
from . import views

urlpatterns = [
    path('works/', views.list_create_poems, name='list_create_poems'),
    path('works/<int:poem_id>/', views.poem_detail, name='poem_detail'),
    path('works/<int:poem_id>/comments/', views.list_create_comments, name='list_create_comments'),
    path('works/<int:poem_id>/like/', views.like_poem, name='like_poem'),
]
