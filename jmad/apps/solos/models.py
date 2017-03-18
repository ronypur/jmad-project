from django.db import models


class Solo(models.Model):
    track = models.CharField(max_length=100, blank=True)
    artist = models.CharField(max_length=100, blank=True)
    instrument = models.CharField(max_length=50, blank=True)
    album = models.CharField(max_length=200, blank=True)
    start_time = models.CharField(max_length=20, blank=True)
    end_time = models.CharField(max_length=20, blank=True)
