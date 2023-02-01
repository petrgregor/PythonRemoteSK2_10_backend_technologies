from django.db import models
from viewer.models import *
import csv
import time
import re

def run():
    new_awards = 0
    i = 7

    with open('data/Staff.csv', encoding="UTF-8") as file:
        reader = csv.reader(file, delimiter=';')  # otevřeme csv soubor

        header = next(reader)  # první řádek je hlavička tabulky
        print(header)

        for row in reader:  # pro další řádky
            awards = row[i].split('|')
            for award in awards:
                print(award)
                try:
                    award_name = re.search(f'\) \((.*?) -', award).group(1)
                    award_category = re.search(r'- (.*?)\)', award).group(1)
                    award_year = re.search(r'\((\d*?)\)', award).group(1)
                    print(f"award_name: '{award_name}', "
                          f"award_category: '{award_category}',"
                          f" award_year: '{award_year}'")
                    movie_name = re.search(f'(.*?) \(', award).group(1).strip()
                    print(f"movie_name: '{movie_name}'")
                    movie = None
                    if movie_name:
                        if Movie.objects.filter(title_orig=movie_name).count() > 0:
                            movie = Movie.objects.get(title_orig=movie_name)
                        elif Movie.objects.filter(title_cz=movie_name).count() > 0:
                            movie = Movie.objects.get(title_cz=movie_name)
                        elif Movie.objects.filter(title_sk=movie_name).count() > 0:
                            movie = Movie.objects.get(title_sk=movie_name)
                    if movie:
                        Award.objects.create(
                            name=award_name,
                            year=award_year,
                            movie=movie,
                            category=award_category
                        )
                        new_awards += 1
                except:
                    print("CHYBA")

    print(f"Konec skriptu '07_add_awards', bylo přidáno {new_awards} nových ocenění.")
