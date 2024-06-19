from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models.users import User
from .models.song import Song
from .models.playlist import Playlist
from .models.history import History

def song_list(request):
    songs = Song.objects.all()
    return render(request, 'karaoke/song_list.html')

@login_required
def order_song(request, song_id):
    song = Song.objects.get(id=song_id)
    Playlist.objects.create(userid=request.user, songid=song, status='pending')
    return redirect('song_list')

@login_required
def order_list(request):
    playlists = Playlist.objects.filter(userid=request.user)
    return render(request, 'karaoke/order_list.html', {'playlists':playlists})