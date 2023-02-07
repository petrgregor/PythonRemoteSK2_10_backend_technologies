from django.test import TestCase
from django.db.utils import IntegrityError

from viewer.models import *
from viewer.views import MovieForm

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

    def test_title_orig_field(self):
        user_input_title_orig = ""
        form = MovieForm(data={'title_orig': user_input_title_orig})
        self.assertFalse(form.is_valid())

    def test_released_field(self):  # TODO: opravit
        year = 1950
        genre = Genre.objects.get(name='Drama')
        country = Country.objects.get(name='CZ')
        form = MovieForm(data={'title_orig': "New movie",
                               'released': 1950,
                               'length': 23,
                               'description': "test",
                               'genre': 1,
                               'country': 1})
        self.assertTrue(form.is_valid())


