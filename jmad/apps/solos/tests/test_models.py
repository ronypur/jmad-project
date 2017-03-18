from django.test import TestCase

from apps.solos.models import Solo


class SoloModelTestCase(TestCase):

    def setUp(self):
        self.solo = Solo.objects.create(
            track='Falling in Love with You',
            artist='Oscar Peterson',
            instrument='piano',
            album='At the Startford Shakespearean Festival',
            start_time='1:24',
            end_time='4:06'
        )

    def test_solo_basic(self):
        """Test basic functionality of Solo"""
        self.assertEqual(self.solo.artist, 'Oscar Peterson')
        self.assertEqual(self.solo.start_time, '1:24')
