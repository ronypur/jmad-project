from django.test import TestCase, RequestFactory
from django.db.models.query import QuerySet

from apps.solos.models import Solo
from apps.solos.views import index, SoloDetailView


class SolosBaseTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpClass(cls):
        super(SolosBaseTestCase, cls).setUpClass()
        cls.drum_solo = Solo.objects.create(
            instrument='drums',
            artist='Rich',
            track='Bugle Call Rag'
        )
        cls.sax_solo = Solo.objects.create(
            instrument='saxophone',
            artist='Coltrane',
            track='Mr. PC'
        )


class IndexViewTestCase(SolosBaseTestCase):

    def test_index_view_basic(self):
        """Test index view returns a 200 response and uses the correct template"""
        request = self.factory.get('/')
        with self.assertTemplateUsed('solos/index.html'):
            response = index(request)
            self.assertEqual(response.status_code, 200)

    def test_index_view_returns_solos(self):
        """Test that the index view will return solos if query parameters exist"""
        response = self.client.get('/', {'instrument': 'drums'})

        solos = response.context['solos']

        self.assertIs(type(solos), QuerySet)
        self.assertEqual(len(solos), 1)
        self.assertEqual(solos[0].artist, 'Rich')


class SoloViewTestCase(SolosBaseTestCase):

    def test_basic(self):
        """
        Solo view return a 200 response, uses the correct template,
        and has the correct context
        :return:
        """
        request = self.factory.get('/solos/1')

        response = SoloDetailView.as_view()(
            request,
            pk=self.drum_solo.pk
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.context_data['solo'].artist,
            'Rich'
        )

        with self.assertTemplateUsed('solos/solo-detail.html'):
            response.render()
