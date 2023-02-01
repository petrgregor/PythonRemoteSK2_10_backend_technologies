from django.db import models
from viewer.models import *
import csv
import time

def run():
    Movie.objects.all().delete()
    new_movies = 0
    with open('data/Movies.csv', encoding="UTF-8") as file:
        reader = csv.reader(file, delimiter=';')  # otevřeme csv soubor

        header = next(reader)  # první řádek je hlavička tabulky

        for row in reader:     # pro další řádky
            age_restr = None
            #Age_restriction
            age_restr = row[10].strip()
            age_restr_number = AgeRestriction.objects.filter(name=age_restr).count()

            if age_restr_number:
                age_r = AgeRestriction.objects.get(name=age_restr)
            else:
                age_r = None

            expanses = None
            if row[8] != "":
                expanses = row[8].strip().replace('$','')\
                    .replace('23,6milióna', '23600000')\
                    .replace(',','')\
                    .replace('milióna','000000').replace('miliónov','000000')
                print(f"expanses: '{expanses}', original value: '{row[8]}'")
                expanses = int(expanses)

            earnings = None
            if row[9] != "":
                earnings = row[9].strip().replace('$','')\
                    .replace('23,6milióna', '23600000')\
                    .replace('370.5 million', '370500000') \
                    .replace('1.489 billion', '1489000000') \
                    .replace('13.9 million', '13900000') \
                    .replace('7.4 million', '7400000')\
                    .replace(',','')\
                    .replace('milióna','000000').replace('miliónov','000000')\
                    .replace(' CZK','')
                print(f"earnings: '{earnings}', original value: '{row[9]}'")
                earnings = int(earnings)

            price = None
            if row[13] != "":
                price = float(row[13])

            title_orig = row[0].strip()
            title_cz = row[1].strip()
            title_sk = row[2].strip()
            movies_set = Movie.objects.filter(title_orig=row[0])

            if not movies_set:
                new_movie = Movie.objects.create(
                    title_orig=title_orig,
                    title_cz=title_cz,
                    title_sk=title_sk,
                    #country
                    #genre
                    released=int(row[5]),
                    length=int(row[6]),
                    description=row[7],
                    expanses=expanses,
                    earnings=earnings,
                    age_restriction=age_r,
                    # images
                    trailer=row[12].strip(),
                    price=price,
                    link=row[14].strip()
                )
                print(f"Do tabulky Movie vložen nový film '{title_orig}'")
                new_movies += 1

                countries = row[3].split('/')
                for country in countries:
                    country_name = country.strip()
                    new_movie.country.add(Country.objects.get(name=country_name))

                genres = row[4].split('/')
                for genre in genres:
                    genre_name = genre.strip()
                    new_movie.genre.add(Genre.objects.get(name=genre_name))

                images = [row[11]]
                for image in images:
                    image_name = image.strip()
                    new_movie.images.add(Image.objects.get(path=image_name))

                new_movie.save()

            else:
                print(f"Nalezený film '{title_orig}' je již v databázi.")

    print(f"Konec skriptu '06_add_movies', bylo přidáno {new_movies} nových filmů.")
