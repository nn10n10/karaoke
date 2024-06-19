from django.db import models
from .users import User
from .song import Song
from .playlist import Playlist

class History(models.Model):
    historyid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.historyid