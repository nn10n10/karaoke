from django.db import models

class Song(models.Model):
    songid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200, null=True, blank=True)
    file_path = models.CharField(max_length=200)
    def __str__(self):
        return self.title
