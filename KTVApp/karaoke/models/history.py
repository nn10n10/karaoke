from django.db import models
from .song import Song
from django.conf import settings
from .playlist import Playlist

class History(models.Model):
    historyid = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.historyid