from django.urls import path
from . import views

urlpatterns = [
    path('songs/', views.song_list, name='song_list'),
    path('order/<int:song_id>/', views.order_song, name='order_song'),
    path('orders/', views.order_list, name='order_list'),
]
