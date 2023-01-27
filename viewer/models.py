from django.db.models import * #Model, CharField, ForeignKey, IntegerField, \
#    DateField, TextField, DateTimeField, DO_NOTHING, CASCADE, SET_NULL, PositiveSmallIntegerField

from django.contrib.auth.models import User

# Create your models here
class Genre(Model):
    name = CharField(max_length=16)

    def __str__(self):
        return self.name


class AgeRestriction(Model):
    name = CharField(max_length=16)

    def __str__(self):
        return self.name


class Country(Model):
    name = CharField(max_length=32)


class AwardCategory(Model):
    name = CharField(max_length=32)


class Staff(Model):
    name = CharField(max_length=16)
    surname = CharField(max_length=16)
    country = ForeignKey(Country, on_delete=SET_NULL)
    date_of_birth = DateField()
    death_date = DateField()
    biography = TextField()
    awards = ManyToMany(Award)


class Image(Model):
    path = CharField(max_length=64)
    description = CharField(max_length=128)


class Movie(Model):
    title_orig = CharField(max_length=64)
    title_cz = CharField(max_length=64)
    title_sk = CharField(max_length=64)
    country = ForeignKey(Country, null=True, on_delete=SET_NULL)
    genre = ForeignKey(Genre, on_delete=SET_NULL)
    released = DateField()
    directors = ManyToManyField(Staff)
    actors = ManyToManyField(Staff)
    length = PositiveIntegerField()
    description = TextField()
    expanses = PositiveIntegerField()
    earnings = PositiveIntegerField()
    age_restriction = ForeignKey(AgeRestriction, on_delete=SET_NULL)
    images = ManyToManyField(Image)
    trailer = CharField(max_length=256)
    price = DecimalField(max_digits=6, decimal_places=2)
    link = CharField(max_length=256)
    created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " (" + str(self.released) + ")"


class Rating(Model):
    movie = ForeignKey(Movie, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=SET_NULL)
    rating = PositiveSmallIntegerField()


class Award(Model):
    name = CharField(max_length=32)
    year = IntegerField()
    movie = ForeignKey(Movie, on_delete=SET_NULL)
    category = ForeignKey(AwardCategory, on_delete=SET_NULL)

