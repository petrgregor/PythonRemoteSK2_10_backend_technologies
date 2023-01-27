from django.db.models import * #Model, CharField, ForeignKey, IntegerField, \
#    DateField, TextField, DateTimeField, DO_NOTHING, CASCADE, SET_NULL, PositiveSmallIntegerField

from django.contrib.auth.models import User

# Create your models here
class Genre(Model):
    name = CharField(max_length=16, null=False, unique=True)

    def __str__(self):
        return self.name


class AgeRestriction(Model):
    name = CharField(max_length=16, null=False, unique=True)

    def __str__(self):
        return self.name


class Country(Model):
    name = CharField(max_length=32, null=False, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class AwardCategory(Model):
    name = CharField(max_length=32, null=False, unique=True)

    def __str__(self):
        return self.name


class Image(Model):
    path = CharField(max_length=64, null=False)
    description = CharField(max_length=128, null=True)

    def __str__(self):
        return self.description[:30]



class Movie(Model):
    title_orig = CharField(max_length=64, null=False)
    title_cz = CharField(max_length=64, null=True)
    title_sk = CharField(max_length=64, null=True)
    country = ForeignKey(Country, null=True, on_delete=SET_NULL)
    genre = ForeignKey(Genre, null=True, on_delete=SET_NULL)
    released = DateField(null=False)
    #directors = ManyToManyField(Staff)
    #actors = ManyToManyField(Staff)
    length = PositiveIntegerField(null=True)
    description = TextField(null=True)
    expanses = PositiveIntegerField(null=True)
    earnings = PositiveIntegerField(null=True)
    age_restriction = ForeignKey(AgeRestriction, null=True, on_delete=SET_NULL)
    images = ManyToManyField(Image)
    trailer = CharField(max_length=256, null=True)
    price = DecimalField(max_digits=6, decimal_places=2, null=True)
    link = CharField(max_length=256, null=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title_orig']

    def __str__(self):
        return self.title + " (" + str(self.released) + ")"


class Rating(Model):
    movie = ForeignKey(Movie, null=False, on_delete=CASCADE)
    user = ForeignKey(User, null=True, on_delete=SET_NULL)
    rating = PositiveSmallIntegerField(null=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['movie', 'created']

    def __str__(self):
        return self.movie.title_orig + " " + self.user.name + " " + self.rating


class Award(Model):
    name = CharField(max_length=32, null=False)
    year = IntegerField(null=False)
    movie = ForeignKey(Movie, null=True, on_delete=SET_NULL)
    category = ForeignKey(AwardCategory, null=True, on_delete=SET_NULL)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', 'category']

    def __str__(self):
        return self.name + " (" + self.year + ") " + self.movie.title_orig


class Staff(Model):
    name = CharField(max_length=16, null=True)
    surname = CharField(max_length=16, null=True)
    artist_name = CharField(max_length=16, null=True)
    country = ForeignKey(Country, null=True, on_delete=SET_NULL)
    date_of_birth = DateField(null=True)
    death_date = DateField(null=True)
    biography = TextField(null=True)
    awards = ManyToManyField(Award)
    directing = ManyToManyField(Movie, related_name='directing_movie')
    acting = ManyToManyField(Movie, related_name='acting_in_movie')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['surname', 'artist_name', 'name']

    def __str__(self):
        return self.name + " " + self.surname + " " + self.artist_name


