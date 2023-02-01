from django.db import models
from viewer.models import *
from datetime import datetime
import csv
import time

def run():
    Staff.objects.all().delete()
    with open('data/Staff.csv', encoding="UTF-8") as file:
        reader = csv.reader(file, delimiter=';')  # otevřeme csv soubor

        header = next(reader)  # první řádek je hlavička tabulky

        for row in reader:     # pro další řádky
            for i in range(len(row)):
                #print(f"{header[i]}: {row[i]}")

                if i == 3:
                    countries = row[i].split('/')
                    # print(f"{header[i]}: {countries}")
                    for country in countries:
                        country_name = country.strip()
                        country_set = Country.objects.filter(name=country_name)
                        if not country_set:
                            Country.objects.create(
                                name=country_name
                            )
                            print(f"Do tabulky Coutry vložena nová země '{country_name}'")

            staff_set = Staff.objects.filter(name=row[0],surname=row[1])
            if not staff_set:
                date_of_birth = datetime.strptime(row[4].strip(), '%d.%m.%Y').date()
                #print(f"{row[4]} = {date_of_birth}")
                death_date = None
                if row[5].strip() != "":
                    death_date = datetime.strptime(row[5].strip(), '%d.%m.%Y').date()
                    #print(f"{row[5]} = {death_date}")
                new_staff = Staff.objects.create(
                    name=row[0].strip(),
                    surname=row[1].strip(),
                    artist_name=row[2].strip(),
                    country=Country.objects.get(name=row[3].strip()),
                    date_of_birth=date_of_birth,
                    death_date=death_date,
                    biography=row[6].strip(),
                    #awards
                    #directing
                    #acting
                )

                """print(row[7])
                awards = row[7].split('|')
                for award in awards:
                    Award.objects.create(
                        name=award,
                    )"""

                #print(row[8])
                movies = row[8].split('|')
                #print(movies)
                for movie in movies:
                    movie_name = movie.strip()
                    movie_set = Movie.objects.filter(title_orig=movie_name)
                    if movie_set:
                        new_staff.directing.add(Movie.objects.get(title_orig=movie_name))

                movies = row[9].split('|')
                #print(movies)
                for movie in movies:
                    movie_name = movie.strip()
                    movie_set = Movie.objects.filter(title_orig=movie_name)
                    if movie_set:
                        new_staff.acting.add(Movie.objects.get(title_orig=movie_name))

                new_staff.save()

        print(header)