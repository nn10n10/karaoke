from django.db import models
from .users import User
from .song import Song

class Playlist(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('playing', 'Playing'),
        ('played', 'Played'),
    ]
    Playid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    songid = models.ForeignKey(Song, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,choices=STATUS_CHOICES,default='pending')

    def __str__(self):
        return f'{self.userid} - {self.songid}'

