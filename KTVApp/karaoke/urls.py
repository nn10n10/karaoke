from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.main, name='main'),
    path('search/', views.search_songs, name='search_songs'),
    path('songs/', views.song_list, name='song_list'),
    path('order/<int:songid>/', views.order_song, name='order_song'),
    path('song/<int:songid>/', views.song_detail, name='song_detail'),
    path('orders/', views.order_list, name='order_list'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main'), name='logout'),
    path('register/', views.register, name='register'),
    path('upload_song/', views.upload_song, name='upload_song'),
]
