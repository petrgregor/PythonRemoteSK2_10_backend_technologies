import time

from django.test import TestCase
from django.db.utils import IntegrityError

# for selenium
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select

from viewer.models import *
from viewer.views import MovieForm, StaffForm

# Create your tests here.
class ExampleTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true")
        self.assertFalse(False)

    def test_add(self):
        print("Method: test_add")
        self.assertEqual(1+1, 2)


class MovieModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        movie = Movie.objects.create(
            title_orig="Test movie orig title",
            title_cz="Test movie title cz",
            title_sk="Test movie title sk",
            released=2023
        )
        country = Country.objects.create(name="CZ")
        movie.country.add(country)
        country_sk = Country.objects.create(name="SK")
        movie.country.add(country_sk)
        genre = Genre.objects.create(name="Drama")
        movie.genre.add(genre)
        movie.save()

        user = User.objects.create(
            username='petrgregor'
        )
        user1 = User.objects.create(
            username='user_no1'
        )

        Rating.objects.create(
            movie=movie,
            user=user,
            rating=5
        )
        Rating.objects.create(
            movie=movie,
            user=user1,
            rating=4
        )


    def test_title_orig(self):
        movie = Movie.objects.get(id=1)
        self.assertEqual(movie.title_orig, "Test movie orig title")

    def test_title_cz(self):
        movie = Movie.objects.get(title_orig="Test movie orig title")
        self.assertEqual(movie.title_cz, "Test movie title cz")

    def test_movie_str(self):
        movie = Movie.objects.get(title_orig="Test movie orig title")
        self.assertEqual(movie.__str__(), "Test movie orig title (2023)")

    def test_movie_average_rating(self):
        movie = Movie.objects.get(id=1)
        avg_rating = Rating.objects.filter(movie=movie).aggregate(Avg('rating'))
        self.assertEqual(avg_rating['rating__avg'], 4.5)

    def test_movie_country_set(self):
        movie = Movie.objects.get(id=1)
        country_count = movie.country.count()
        self.assertEqual(country_count, 2)


class GenreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name='Drama')

    def test_genre_unique(self):
        with self.assertRaises(IntegrityError):
            Genre.objects.create(name='Drama')


class MovieFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name='Drama')
        Country.objects.create(name='CZ')
        AgeRestriction.objects.create(name='18+')

    def test_title_orig_field(self):
        user_input_title_orig = ""
        form = MovieForm(data={'title_orig': user_input_title_orig,
                               'title_cz': 'Nový film',
                               'title_sk': 'Nový film',
                               'country': ['1'],
                               'genre': ['1'],
                               'released': '1950',
                               'length': '123',
                               'description': 'test',
                               'expanses': '10',
                               'earnings': '20',
                               'age_restriction': '1',
                               'images': [],
                               'trailer': '',
                               'price': '12.5',
                               'link': ''})
        self.assertFalse(form.is_valid())

    def test_released_field(self):
        genre = Genre.objects.get(name='Drama')
        country = Country.objects.get(name='CZ')

        form = MovieForm(data={'title_orig': 'New movie',
                               'title_cz': 'Nový film',
                               'title_sk': 'Nový film',
                               'country': ['1'],
                               'genre': ['1'],
                               'released': '1950',
                               'length': '123',
                               'description': 'test',
                               'expanses': '10',
                               'earnings': '20',
                               'age_restriction': '1',
                               'images': [],
                               'trailer': '',
                               'price': '12.5',
                               'link': ''})
        self.assertTrue(form.is_valid())

    def test_released_in_the_past_field(self):
        genre = Genre.objects.get(name='Drama')
        country = Country.objects.get(name='CZ')

        form = MovieForm(data={'title_orig': 'New movie',
                               'title_cz': 'Nový film',
                               'title_sk': 'Nový film',
                               'country': ['1'],
                               'genre': ['1'],
                               'released': '1850',
                               'length': '123',
                               'description': 'test',
                               'expanses': '10',
                               'earnings': '20',
                               'age_restriction': '1',
                               'images': [],
                               'trailer': '',
                               'price': '12.5',
                               'link': ''})
        self.assertFalse(form.is_valid())


    def test_released_in_the_future_field(self):
        genre = Genre.objects.get(name='Drama')
        country = Country.objects.get(name='CZ')

        form = MovieForm(data={'title_orig': 'New movie',
                               'title_cz': 'Nový film',
                               'title_sk': 'Nový film',
                               'country': ['1'],
                               'genre': ['1'],
                               'released': '2025',
                               'length': '123',
                               'description': 'test',
                               'expanses': '10',
                               'earnings': '20',
                               'age_restriction': '1',
                               'images': [],
                               'trailer': '',
                               'price': '12.5',
                               'link': ''})
        self.assertFalse(form.is_valid())

class StaffFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Country.objects.create(name='CZ')

    def test_name_field(self):
        form = StaffForm(data={'name': 'Petr',
                               'country': '1'})
        self.assertTrue(form.is_valid())


# Selenium
# pip install selenium
class StaffFormTestWithSelenium(LiveServerTestCase):

    def test_sign_up_and_login(self):
        selenium = webdriver.Chrome()
        # Choose your url to visit
        selenium.get('http://127.0.0.1:8000/')
        # find the elements you need to submit form
        login = selenium.find_element(By.ID, 'id_login')
        login.click()
        time.sleep(2)

        sign_up = selenium.find_element(By.ID, 'id_sign_up')
        sign_up.click()
        time.sleep(2)

        username = selenium.find_element(By.ID, 'id_username')
        password1 = selenium.find_element(By.ID, 'id_password1')
        password2 = selenium.find_element(By.ID, 'id_password2')
        username.send_keys('TestUser')
        password1.send_keys('MyTestPassword')
        password2.send_keys('MyTestPassword')
        submit = selenium.find_element(By.ID, 'id_submit')
        submit.send_keys(Keys.RETURN)
        time.sleep(2)

        login = selenium.find_element(By.ID, 'id_login')
        login.click()
        time.sleep(2)

        username = selenium.find_element(By.ID, 'id_username')
        password = selenium.find_element(By.ID, 'id_password')

        username.send_keys('TestUser')
        password.send_keys('MyTestPassword')
        time.sleep(2)

        submit = selenium.find_element(By.ID, 'id_submit')
        submit.send_keys(Keys.RETURN)
        time.sleep(2)

        assert 'Welcome in our movie database.' in selenium.page_source


    def test_add_new_staff(self):
        selenium = webdriver.Chrome()
        # Choose your url to visit
        selenium.get('http://127.0.0.1:8000/')
        # find the elements you need to submit form
        login = selenium.find_element(By.ID, 'id_login')
        login.click()
        time.sleep(2)

        username = selenium.find_element(By.ID, 'id_username')
        password = selenium.find_element(By.ID, 'id_password')

        username.send_keys('User1')
        password.send_keys('mojeheslo')
        time.sleep(2)

        submit = selenium.find_element(By.ID, 'id_submit')
        submit.send_keys(Keys.RETURN)
        time.sleep(2)

        new_staff_link = selenium.find_element(By.ID, 'id_new_staff_link')
        new_staff_link.click()
        time.sleep(2)

        name = selenium.find_element(By.ID, 'id_name')
        surname = selenium.find_element(By.ID, 'id_surname')
        artistname = selenium.find_element(By.ID, 'id_artist_name')
        county = selenium.find_element(By.ID, 'id_country')
        time.sleep(1)
        name.send_keys('Martin')
        time.sleep(1)
        surname.send_keys('Novák')
        time.sleep(1)
        artistname.send_keys('Novy')
        time.sleep(1)
        select_country = Select(selenium.find_element(By.ID, 'id_country'))
        time.sleep(1)
        select_country.select_by_visible_text('CZ')
        time.sleep(1)

        submit = selenium.find_element(By.ID, 'id_submit')
        submit.send_keys(Keys.RETURN)
        time.sleep(2)

        assert 'Add new staff' in selenium.page_source
