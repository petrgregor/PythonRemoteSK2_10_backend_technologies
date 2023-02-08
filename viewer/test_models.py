from django.test import TestCase
from django.db.utils import IntegrityError

from viewer.models import *


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
