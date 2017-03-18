from django.test import TestCase, RequestFactory
from django.db.models.query import QuerySet

from apps.solos.models import Solo
from apps.solos.views import index, SoloDetailView
from apps.albums.models import Album, Track


class SolosBaseTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpClass(cls):
        super(SolosBaseTestCase, cls).setUpClass()
        cls.no_funny_hats = Album.objects.create(
            name='No Funny Hats', slug='no-funny-hats'
        )
        cls.bugle_call_rag = Track.objects.create(
            name='Bugle Call Rag', slug='bugle-call-rag', album=cls.no_funny_hats
        )
        cls.drum_solo = Solo.objects.create(
            instrument='drums', artist='Rich',
            track=cls.bugle_call_rag, slug='rich'
        )

        cls.giant_step = Album.objects.create(
            name='Giant Step', slug='giant-step'
        )
        cls.mr_pc = Track.objects.create(
            name='Mr. PC', slug='mr-pc', album=cls.giant_step
        )
        cls.sax_solo = Solo.objects.create(
            instrument='saxophone', artist='Coltrane',
            track=cls.mr_pc, slug='coltrane'
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

        with self.assertTemplateUsed('solos/solo_detail.html'):
            response.render()
