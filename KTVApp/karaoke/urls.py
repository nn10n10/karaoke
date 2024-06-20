from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_songs, name='search_songs'),
    path('songs/', views.song_list, name='song_list'),
    path('order/<int:song_id>/', views.order_song, name='order_song'),
    path('orders/', views.order_list, name='order_list'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
