from django.test import TestCase
from django.db.utils import IntegrityError

from viewer.models import *
from viewer.views import MovieForm, StaffForm


class MovieFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name='Drama')
        Genre.objects.create(name='Krimi')
        Country.objects.create(name='CZ')
        AgeRestriction.objects.create(name='18+')

    def test_title_orig_field(self):
        user_input_title_orig = ""
        form = MovieForm(data={'title_orig': user_input_title_orig,
                               'title_cz': 'Nový film',
                               'title_sk': 'Nový film',
                               'country': ['1'],
                               'genre': ['1', '2'],
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
        form = MovieForm(data={'title_orig': 'New movie',
                               'title_cz': 'Nový film',
                               'title_sk': 'Nový film',
                               'country': ['1'],
                               'genre': ['1'],
                               'released': '1980',
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

