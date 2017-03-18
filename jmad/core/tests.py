from django.test import LiveServerTestCase

from selenium import webdriver

from apps.solos.models import Solo


class StudentTestCase(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(2)

        self.solo1 = Solo.objects.create(
            instrument='saxophone',
            artist='Jhon Coltrane',
            track='My Favorite Things',
            album='My Favorite Things'
        )

        self.solo2 = Solo.objects.create(
            instrument='saxophone',
            artist='Cannonball Adderley',
            track='All Blues',
            album='Kind of Blue',
            start_time='2:06',
            end_time='4:01'
        )

        self.solo3 = Solo.objects.create(
            instrument='saxophone',
            artist='Cannonball Adderley',
            track='Waltz for Debby',
            album='Know What I Mean?'
        )

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

        # Redirecting to solo detail view
        self.assertEqual(self.browser.current_url, '{}/solos/7/'.format(self.live_server_url))

        # Seeing the artist name
        self.assertEqual(
            self.browser.find_element_by_css_selector('#jmad-artist').text,
            'Cannonball Adderley')

        # Seeing the track
        self.assertEqual(
            self.browser.find_element_by_css_selector('#jmad-track').text,
            'All Blues')

        # Seeing the instrument
        self.assertEqual(
            self.browser.find_element_by_css_selector('#jmad-album').text,
            'Kind of Blue')

        # Seeing artist start and end time of the show
        self.assertEqual(
            self.browser.find_element_by_css_selector('#jmad-start-time').text,
            '2:06')
        self.assertEqual(
            self.browser.find_element_by_css_selector('#jmad-end-time').text,
            '4:01')

        # This test is incomplete
        self.fail('incomplete test')