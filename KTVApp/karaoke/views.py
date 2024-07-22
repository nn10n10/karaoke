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
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone

@ensure_csrf_cookie
def main(request):
    # Get the first song with 'playing' status from the Playlist
    current_playlist_item = Playlist.objects.filter(status='playing').first()
    current_song = current_playlist_item.songid if current_playlist_item else None

    # If no song is playing, get the first pending song
    if not current_song:
        pending_playlist_item = Playlist.objects.filter(status='pending').first()
        if pending_playlist_item:
            pending_playlist_item.status = 'playing'
            pending_playlist_item.save()
            current_song = pending_playlist_item.songid
            
    context = {
        'current_song': current_song,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'main.html', context)

@require_POST
def song_ended(request):
    finished_song = Playlist.objects.filter(status='playing').first()
    if finished_song:
        # 添加到历史记录
        History.objects.create(
            user=finished_song.userid,
            song=finished_song.songid,
            order_time=timezone.now()
        )
        # 删除已播放的歌曲
        finished_song.delete()

    next_song = Playlist.objects.filter(status='pending').first()
    if next_song:
        next_song.status = 'playing'
        next_song.save()
    
    return JsonResponse({'success': True})

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
            return redirect('main')
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
        messages.success(request, f"{song.title} has been added to the playlist.")
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

@login_required
def view_history(request):
    user_history = History.objects.filter(user=request.user).order_by('-order_time')
    context = {
        'history': user_history
    }
    return render(request, 'history.html', context)


def logout_view(request):
    logout(request)
    return redirect('main')