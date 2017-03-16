from django.db import models


class Solo(models.Model):
    track = models.CharField(max_length=100, blank=True)
    artist = models.CharField(max_length=100, blank=True)
    instrument = models.CharField(max_length=50, blank=True)
