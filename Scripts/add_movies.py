from django.db import models
from viewer.models import *
import csv
import time

def run():
    with open('data/Movies.csv', encoding="UTF-8") as file:
        reader = csv.reader(file, delimiter=';')  # otevřeme csv soubor

        header = next(reader)  # první řádek je hlavička tabulky

        for row in reader:     # pro další řádky
            for i in range(len(row)):
                age_restr = None
                if i == 3:
                    countries = row[i].split('/')
                    #print(f"{header[i]}: {countries}")
                    for country in countries:
                        country_name = country.strip()
                        country_set = Country.objects.filter(name=country_name)
                        if not country_set:
                            Country.objects.create(
                                name=country_name
                            )
                            print(f"Do tabulky Coutry vložena nová země '{country_name}'")
                elif i == 4:
                    genres = row[i].split('/')
                    #print(f"{header[i]}: {genres}")
                    for genre in genres:
                        genre_name = genre.strip()
                        genre_set = Genre.objects.filter(name=genre_name)
                        if not genre_set:
                            Genre.objects.create(
                                name=genre_name
                            )
                            print(f"Do tabulky Genre vložen nový žánr '{genre_name}'")
                elif i == 5:
                    released = int(row[i])
                    #print(f"{header[i]}: {released}")
                elif i == 10:  #Age_restriction
                    age_restr = row[i].strip()
                    age_restr_set = AgeRestriction.objects.filter(name=age_restr)
                    if not age_restr_set:
                        AgeRestriction.objects.create(
                            name=age_restr
                        )
                        print(f"Do tabulky AgeRestriction vložno {age_restr}")
                elif i == 11:
                    images = row[i].strip()
                    #print(f"images: {images}")
                    images_set = Image.objects.filter(path=images)
                    if not images_set:
                        Image.objects.create(
                            path=images,
                            description=""
                        )
                        print(f"Vložen obrázek {images}")
                else:
                    pass
                    #print(f"{header[i]}: {row[i]}")

                age_r = AgeRestriction.objects.filter(name=age_restr)
                if not age_r:
                    age_r = None

                expanses = None
                """if row[8] != "":
                    expanses = int(row[8])"""

                earnings = None
                """if row[9] != "":
                    earnings = int(row[9])"""

                price = None
                if row[13] != "":
                    price = float(row[13])

                movies_set = Movie.objects.filter(title_orig=row[0])

                if not movies_set:
                    time.sleep(1)
                    new_movie = Movie.objects.create(
                        title_orig=row[0],
                        title_cz=row[1],
                        title_sk=row[2],
                        #country
                        #genre
                        released=row[5],
                        length=row[6],
                        description=row[7],
                        expanses=expanses,
                        earnings=earnings,
                        age_restriction=age_r,
                        # images
                        trailer=row[12],
                        price=price,
                        link=row[14]
                    )

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
                        print(image_name)
                        new_movie.images.add(Image.objects.get(path=image_name))

                    new_movie.save()

        print(header)
run()