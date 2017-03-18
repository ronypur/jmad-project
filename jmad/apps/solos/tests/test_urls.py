from django.test import TestCase
from django.core.urlresolvers import resolve

from apps.solos.views import index


class SolosURLsTestCase(TestCase):

    def test_root_url_uses_index_view(self):
        """Test that the root of the site resolve to the correct view function"""
        root = resolve('/')

        self.assertEqual(root.func, index)

    def test_solo_detail_view(self):
        """Test that the URL for SoloDetail resolve to correct view function"""
        solo_detail = resolve('/solos/1/')

        self.assertEqual(solo_detail.func.__name__, 'SoloDetailView')
        self.assertEqual(solo_detail.kwargs['pk'], '1')
