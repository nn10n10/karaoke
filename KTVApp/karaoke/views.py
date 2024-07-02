from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models.song import Song
from .models.playlist import Playlist
from .models.history import History
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .forms import SongForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

def admin_required(user):
    return user.is_staff

def search_songs(request):
    query = request.GET.get('q', '').strip()
    page = request.GET.get('page', 1)
    results_per_page = 20 

    if query:
        songs = Song.objects.filter(
            Q(title__icontains=query) |
            Q(artist__icontains=query) |
            Q(album__icontains=query)
        ).distinct().order_by('title')
    else:
        songs = Song.objects.all().order_by('title')[:100]  

    paginator = Paginator(songs, results_per_page)
    try:
        songs_page = paginator.page(page)
    except PageNotAnInteger:
        songs_page = paginator.page(1)
    except EmptyPage:
        songs_page = paginator.page(paginator.num_pages)

    context = {
        'songs': songs_page,
        'query': query,
        'is_paginated': songs_page.has_other_pages(),
    }

    if not songs and query:
        messages.info(request, "結果がありませんでした")

    return render(request, 'search_songs.html', context)

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
def order_song(request, songid):
    if request.method == 'POST':
        song = get_object_or_404(Song, songid=songid)
        Playlist.objects.create(userid=request.user, songid=song, status='pending')
        return redirect('song_detail', songid=songid)
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

def song_detail(request, songid):
    song = get_object_or_404(Song, songid=songid)
    return render(request, 'song_detail.html', {'song': song})