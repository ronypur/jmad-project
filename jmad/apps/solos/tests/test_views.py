from django.test import TestCase, RequestFactory

from apps.solos.views import index


class IndexViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view_basic(self):
        """Test index view returns a 200 response and uses the correct template"""
        request = self.factory.get('/')
        response = index(request)
        self.assertEqual(response.status_code, 200)