from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model

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
            instrument='saxophone', artist='John Coltrane',
            track=self.track1, slug='john-coltrane'
        )

        self.album2 = Album.objects.create(
            name='Kind of Blue', slug='kind-of-blue'
        )
        self.track2 = Track.objects.create(
            name='All Blues', slug='all-blues',
            album=self.album2, track_number=4
        )
        self.solo2 = Solo.objects.create(
            instrument='saxophone', artist='Cannonball Adderley',
            track=self.track2, start_time='4:05',
            end_time='6:04', slug='cannonball-adderley'
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

        self.track4 = Track.objects.create(
            name='Freddie Freeloader', slug='freddie-freeloader',
            album=self.album2, track_number=2
        )
        self.solo4 = Solo.objects.create(
            instrument='trumpet', artist='Miles Davis',
            track=self.track2, slug='miles-davis',
            start_time='1:46', end_time='4:04'
        )

        self.track5 = Track.objects.create(
            name='Blue in Green', slug='blue-in-green',
            album=self.album2, track_number=3
        )

        self.admin_user = get_user_model().objects.create_superuser(
            username='bill',
            email='bill@example.com',
            password='password'
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
        self.browser.get(self.live_server_url + '/')

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
            '4:05')
        self.assertEqual(
            self.browser.find_element_by_css_selector('#jmad-end-time').text,
            '6:04')

    def test_staff_can_add_content(self):
        """Tests that a 'staff' user can access the admin and adds Albums, Tracks, and Solos"""
        # John would like to add a record and a number of solos to JMAD.
        # He visits the admin site
        self.browser.get(self.live_server_url + '/admin/')

        # He can tell he's in the right place because of the page title
        self.assertEqual(self.browser.title, 'Log in | Django site admin')

        # He enters his username and password and submits the form to log in
        login_form = self.browser.find_element_by_id('login-form')
        login_form.find_element_by_name('username').send_keys('bill')
        login_form.find_element_by_name('password').send_keys('password')
        login_form.find_element_by_css_selector('.submit-row input').click()

        # He sees links to Albums, Tracks, and Solos
        album_links = self.browser.find_elements_by_link_text('Albums')
        self.assertEqual(
            album_links[0].get_attribute('href'),
            self.live_server_url + '/admin/albums/album/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text('Tracks').get_attribute('href'),
            self.live_server_url + '/admin/albums/track/'
        )

        solos_link = self.browser.find_elements_by_link_text('Solos')
        self.assertEqual(
            solos_link[0].get_attribute('href'),
            self.live_server_url + '/admin/solos/solo/'
        )

        # He clicks on Albums and sees all of the Albums that have been
        # added so far
        album_links[0].click()
        self.assertEqual(
            self.browser.find_element_by_link_text('Know What I Mean?').get_attribute('href'),
            self.live_server_url + '/admin/albums/album/10/change/'
        )
        self.assertEqual(
            self.browser.find_element_by_link_text('Kind of Blue').get_attribute('href'),
            self.live_server_url + '/admin/albums/album/9/change/'
        )
        self.assertEqual(
            self.browser.find_element_by_link_text('My Favorite Things').get_attribute('href'),
            self.live_server_url + '/admin/albums/album/8/change/'
        )

        # Going back to the homepage, he clicks the Tracks link and sees
        # the Tracks that have been added. They're ordered first by Album,
        # then by the track number
        self.browser.find_element_by_css_selector('#site-name a').click()
        self.browser.find_element_by_link_text('Tracks').click()

        track_rows = self.browser.find_elements_by_css_selector('#result_list tr')
        self.assertEqual(track_rows[1].text, 'Kind of Blue Freddie Freeloader 2')
        self.assertEqual(track_rows[2].text, 'Kind of Blue Blue in Green 3')
        self.assertEqual(track_rows[3].text, 'Kind of Blue All Blues 4')
        self.assertEqual(track_rows[4].text, 'Know What I Mean? Waltz for Debby -')
        self.assertEqual(track_rows[5].text, 'My Favorite Things My Favorite Things -')

        # He adds track to an album that already exists
        self.browser.find_element_by_link_text('ADD TRACK').click()

        track_form = self.browser.find_element_by_id('track_form')

        track_form.find_element_by_name('name').send_keys('So What')
        track_form.find_element_by_name('album').find_elements_by_tag_name('option')[1].click()
        track_form.find_element_by_name('track_number').send_keys(1)
        track_form.find_element_by_name('slug').send_keys('so-what')
        track_form.find_elements_by_css_selector('.submit-row input')[0].click()

        self.assertEqual(
            self.browser.find_elements_by_css_selector('#result_list tr')[1].text,
            'Kind of Blue So What 1'
        )

        # He adds another track, this time on an album that is not in JMAD yet
        self.browser.find_element_by_link_text('ADD TRACK').click()

        track_form = self.browser.find_element_by_id('track_form')

        track_form.find_element_by_name('name').send_keys('My Funny Valentine')

        # After adding the basic info, he clicks on the plus sign
        # to add a new album
        track_form.find_element_by_id('add_id_album').click()

        # Fhe focus shifts to the newly opened window, where
        # he sees an Album form
        self.browser.switch_to.window(self.browser.window_handles[1])

        album_form = self.browser.find_element_by_id('album_form')

        album_form.find_element_by_name('name').send_keys('Cookin\'')
        album_form.find_element_by_name('artist').send_keys('Miles Davis Quintet')
        album_form.find_element_by_name('slug').send_keys('cookin')
        album_form.find_element_by_css_selector('.submit-row input').click()

        # After creating the Album , he goes back to finish the Track
        self.browser.switch_to.window(self.browser.window_handles[0])

        track_form = self.browser.find_element_by_id('track_form')

        track_form.find_element_by_name('track_number').send_keys(1)
        track_form.find_element_by_name('slug').send_keys('my-funny-valentine')
        track_form.find_elements_by_css_selector('.submit-row input')[0].click()

        self.assertEqual(
            self.browser.find_elements_by_css_selector('#result_list tr')[1].text,
            'Cookin\' My Funny Valentine 1'
        )

        # He goes back to the root of the admin site and clicks on 'Solos'
        self.browser.find_element_by_css_selector('#site-name a').click()
        self.browser.find_element_by_link_text('Solos').click()

        # He sees Solos listed by Album, then Tracks, then start time
        solo_rows = self.browser.find_elements_by_css_selector('#result_list tr')

        self.assertEqual(solo_rows[1].text, 'All Blues Miles Davis 1:46-4:04')
        self.assertEqual(solo_rows[2].text, 'All Blues Cannonball Adderley 4:05-6:04')
        self.assertEqual(solo_rows[3].text.strip(), 'Waltz for Debby Cannonball Adderley')
        self.assertEqual(solo_rows[4].text.strip(), 'My Favorite Things John Coltrane')

        # He added a Solo to a Track that already exists
        self.browser.find_element_by_link_text('ADD SOLO').click()

        solo_form = self.browser.find_element_by_id('solo_form')

        solo_form.find_element_by_name('track').find_elements_by_tag_name('option')[7].click()
        solo_form.find_element_by_name('artist').send_keys('McCoy Tyner')
        solo_form.find_element_by_name('instrument').send_keys('Piano')
        solo_form.find_element_by_name('start_time').send_keys('2:19')
        solo_form.find_element_by_name('end_time').send_keys('7:01')
        solo_form.find_element_by_name('slug').send_keys('mccoy-tyner')
        solo_form.find_elements_by_css_selector('.submit-row input')[0].click()

        self.assertEqual(
            self.browser.find_elements_by_css_selector('#result_list tr')[5].text,
            'My Favorite Things McCoy Tyner 2:19-7:01'
        )

        # He then adds a Solo for which the Track and Album
        # do not yet exists
        self.browser.find_element_by_link_text('ADD SOLO').click()

        # He adds Track from the Solo page
        self.browser.find_element_by_id('add_id_track').click()

        self.browser.switch_to.window(self.browser.window_handles[1])

        track_form = self.browser.find_element_by_id('track_form')
        track_form.find_element_by_name('name').send_keys('In Walked Bud')

        # He adds Album from the Track popup
        self.browser.find_element_by_id('add_id_album').click()

        self.browser.switch_to.window(self.browser.window_handles[2])

        album_form = self.browser.find_element_by_id('album_form')
        album_form.find_element_by_name('name').send_keys('Misterioso')
        album_form.find_element_by_name('artist').send_keys('Thelonious Monk Quartet')
        album_form.find_element_by_name('slug').send_keys('misterioso')
        album_form.find_element_by_css_selector('.submit-row input').click()

        # He finishes up both parent objects, and save the Solo
        self.browser.switch_to.window(self.browser.window_handles[1])

        track_form = self.browser.find_element_by_id('track_form')
        track_form.find_element_by_name('track_number').send_keys('4')
        track_form.find_element_by_name('slug').send_keys('in-walked-bud')
        track_form.find_element_by_css_selector('.submit-row input').click()

        self.browser.switch_to.window(self.browser.window_handles[0])

        solo_form = self.browser.find_element_by_id('solo_form')
        solo_form.find_element_by_name('artist').send_keys('Johnny Griffin')
        solo_form.find_element_by_name('instrument').send_keys('Tenor Saxophone')
        solo_form.find_element_by_name('start_time').send_keys('0:59')
        solo_form.find_element_by_name('end_time').send_keys('6:21')
        solo_form.find_element_by_name('slug').send_keys('johnny-griffin')
        solo_form.find_elements_by_css_selector('.submit-row input')[0].click()

        self.assertEqual(
            self.browser.find_elements_by_css_selector('#result_list tr')[4].text,
            'In Walked Bud Johnny Griffin 0:59-6:21'
        )

        # This test is incomplete
        self.fail('incomplete test')