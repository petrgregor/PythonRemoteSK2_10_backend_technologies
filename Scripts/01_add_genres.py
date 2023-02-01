from django.db import models
from viewer.models import *
import csv
import time

def run():
    new_genres = 0
    i = 4

    with open('data/Movies.csv', encoding="UTF-8") as file:
        reader = csv.reader(file, delimiter=';')  # otevřeme csv soubor

        header = next(reader)  # první řádek je hlavička tabulky

        for row in reader:     # pro další řádky
            genres = row[i].split('/')
            for genre in genres:
                genre_name = genre.strip()
                genre_set = Genre.objects.filter(name=genre_name)
                if not genre_set:
                    Genre.objects.create(
                        name=genre_name
                    )
                    print(f"Do tabulky Genre vložen nový žánr '{genre_name}'")
                    new_genres += 1
                else:
                    print(f"Nalezený žánr '{genre_name}' je již v databázi.")

    print(f"Konec skriptu '01_add_genres', bylo přidáno {new_genres} nových žánrů.")