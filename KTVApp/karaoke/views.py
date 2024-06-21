from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models.users import User
from .models.song import Song
from .models.playlist import Playlist
from .models.history import History
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .forms import SongForm
from django.contrib.auth.decorators import user_passes_test

def admin_required(user):
    return user.is_staff

def search_songs(request):
    query = request.GET.get('q')
    if query:
        songs = Song.objects.filter(
            Q(title__icontains=query) |
            Q(artist__icontains=query) |
            Q(album__icontains=query)
        )
    else:
        songs = Song.objects.none()
    return render(request, 'search_songs.html', {'songs': songs, 'query': query})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('song_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('song_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def song_list(request):
    songs = Song.objects.all()
    return render(request, 'song_list.html')

@login_required
def order_song(request, song_id):
    song = Song.objects.get(id=song_id)
    Playlist.objects.create(userid=request.user, songid=song, status='pending')
    return redirect('song_list')

@login_required
def order_list(request):
    playlists = Playlist.objects.filter(userid=request.user)
    return render(request, 'order_list.html', {'playlists':playlists})

@login_required
@user_passes_test(admin_required)
def upload_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('song_list')
    else:
        form = SongForm()
    return render(request, 'upload_song.html', {'form': form})