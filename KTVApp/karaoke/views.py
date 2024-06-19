from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User, Song, Playlist, History

def song_list(request):
    songs = Song.objects.all()
    return render(request, 'karaoke/song_list.html')

