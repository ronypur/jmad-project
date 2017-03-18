from django.test import LiveServerTestCase

from selenium import webdriver

from apps.solos.models import Solo
from apps.albums.models import Album, Track


class StudentTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(2)

        self.album1 = Album.objects.create(
            name='My Favorite Things', slug='my-favorite-things'
        )
        self.track1 = Track.objects.create(
            name='My Favorite Things', slug='my-favorite-things',
            album=self.album1
        )
        self.solo1 = Solo.objects.create(
            instrument='saxophone', artist='Jhon Coltrane',
            track=self.track1, slug='jhon-coltrane'
        )

        self.album2 = Album.objects.create(
            name='Kind of Blue', slug='kind-of-blue'
        )
        self.track2 = Track.objects.create(
            name='All Blues', slug='all-blues',
            album=self.album2
        )
        self.solo2 = Solo.objects.create(
            instrument='saxophone', artist='Cannonball Adderley',
            track=self.track2, start_time='2:06',
            end_time='4:01', slug='cannonball-adderley'
        )

        self.album3 = Album.objects.create(
            name='Know What I Mean?', slug='know-what-i-mean'
        )
        self.track3 = Track.objects.create(
            name='Waltz for Debby', slug='waltz-for-debby',
            album=self.album3
        )
        self.solo3 = Solo.objects.create(
            instrument='saxophone', artist='Cannonball Adderley',
            track=self.track3, slug='cannonball-adderley'
        )

        self.track4 = Track.objects.create(name='Freddie Freeloader', slug='freddie-freeloader', album=self.album2)
        self.solo4 = Solo.objects.create(
            instrument='trumpet', artist='Miles Davis',
            track=self.track2, slug='miles-davis'
        )

        self.track5 = Track.objects.create(name='Blue in Green', slug='blue-in-green', album=self.album2)

    def tearDown(self):
        self.browser.quit()

    def find_search_results(self):
        return self.browser.find_elements_by_css_selector(
            '.jmad-search-result a'
        )

    def test_student_find_solos(self):
        """Test that a student can search for solos"""
        # Visit homepage of JMAD
        homepage = self.browser.get(self.live_server_url + '/')

        # JMAD shown in the homepage heading
        brand_element = self.browser.find_element_by_css_selector('.navbar-brand')
        self.assertEqual('JMAD', brand_element.text)

        # Search form, including label and placeholder is exists
        # in homepage
        instrument_input = self.browser.find_element_by_css_selector('input#jmad-instrument')
        self.assertIsNotNone(self.browser.find_element_by_css_selector('label[for="jmad-instrument"]'))
        self.assertEqual(instrument_input.get_attribute('placeholder'), 'i.e. trumpet')

        artist_input = self.browser.find_element_by_css_selector('input#jmad-artist')
        self.assertIsNotNone(self.browser.find_element_by_css_selector('label[for="jmad-artist"]'))
        self.assertEqual(artist_input.get_attribute('placeholder'), 'i.e. Davis')

        # Typing the name of the instrument and click the submit button
        instrument_input.send_keys('saxophone')
        self.browser.find_element_by_css_selector('form button').click()

        # Too many search results, need to add a particular artist
        # to search query
        search_results = self.find_search_results()
        self.assertGreater(len(search_results), 2)

        # Adding a particular artist in search query and
        # get more manageable result
        second_artist_input = self.browser.find_element_by_css_selector('input#jmad-artist')
        second_artist_input.send_keys('Cannonball Adderley')
        self.browser.find_element_by_css_selector('form button').click()

        second_search_results = self.find_search_results()
        self.assertEqual(len(second_search_results), 2)

        # Clicking on search result
        second_search_results[0].click()

        # On the solo page
        self.assertEqual(
            self.browser.current_url,
            '{}/recordings/kind-of-blue/all-blues/cannonball-adderley/'.format(self.live_server_url)
        )

        # Seeing the artist name
        self.assertEqual(
            self.browser.find_element_by_css_selector('#jmad-artist').text,
            'Cannonball Adderley')

        # Seeing the track title (with count of solo)
        self.assertEqual(
            self.browser.find_element_by_css_selector('#jmad-track').text,
            'All Blues [2 solos]')

        # Seeing the album
        self.assertEqual(
            self.browser.find_element_by_css_selector('#jmad-album').text,
            'Kind of Blue [3 tracks]')

        # Seeing artist start and end time of the show
        self.assertEqual(
            self.browser.find_element_by_css_selector('#jmad-start-time').text,
            '2:06')
        self.assertEqual(
            self.browser.find_element_by_css_selector('#jmad-end-time').text,
            '4:01')

        # This test is incomplete
        self.fail('incomplete test')