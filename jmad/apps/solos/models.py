from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify

import musicbrainzngs as mb

from apps.albums.models import Album, Track


mb.set_useragent('JMAD - http://jmad.us', version='0.0.1')


class Solo(models.Model):
    track = models.ForeignKey(Track)
    artist = models.CharField(max_length=100)
    instrument = models.CharField(max_length=50)
    start_time = models.CharField(max_length=20, blank=True)
    end_time = models.CharField(max_length=20, blank=True)
    slug = models.SlugField()

    class Meta:
        ordering = ['track', 'start_time']

    @classmethod
    def get_artist_tracks_from_musicbrainz(cls, artist):
        search_results = mb.search_artists(artist)
        best_result = search_results['artist-list'][0]
        instrument = Solo.get_instrument_from_musicbrainz_tags(best_result['tag-list'])

        for album_dict in mb.browse_releases(best_result['id'], includes=['recordings'])['release-list']:
            album = Album.objects.create(
                name=album_dict['title'],
                artist=artist,
                slug=slugify(album_dict['title'])
            )

            for track_dict in album_dict['medium-list']:
                track = Track.objects.create(
                    album=album,
                    name=track_dict['recording']['title'],
                    track_number=track_dict['position'],
                    slug=slugify(track_dict['recording'['title']])
                )

                Solo.objects.create(
                    track=track, artist=artist,
                    instrument=instrument, slug=slugify(artist)
                )

        return Solo.objects.filter(artist=artist)

    def get_absolute_url(self):
        return reverse('solo_detail_view', kwargs={
            'album': self.track.album.slug,
            'track': self.track.slug,
            'artist': self.slug
        })

    def get_duration(self):
        duration_string = ''
        if self.start_time and self.end_time:
            duration_string = '{}-{}'.format(self.start_time, self.end_time)
        return duration_string