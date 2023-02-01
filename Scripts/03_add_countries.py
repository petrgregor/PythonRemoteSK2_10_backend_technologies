from django.db import models
from viewer.models import *
import csv
import time


def run():
    new_countries = 0
    i = 3

    with open('data/Movies.csv', encoding="UTF-8") as file:
        reader = csv.reader(file, delimiter=';')  # otevřeme csv soubor

        header = next(reader)  # první řádek je hlavička tabulky

        for row in reader:  # pro další řádky
            countries = row[i].split('/')
            for country in countries:
                country_name = country.strip()
                country_set = Country.objects.filter(name=country_name)
                if not country_set:
                    Country.objects.create(
                        name=country_name
                    )
                    print(f"Do tabulky Coutry vložena nová země '{country_name}'")
                    new_countries += 1
                else:
                    print(f"Nalezená země '{country_name}' je již v databázi.")

    with open('data/Staff.csv', encoding="UTF-8") as file:
        reader = csv.reader(file, delimiter=';')  # otevřeme csv soubor

        header = next(reader)  # první řádek je hlavička tabulky

        for row in reader:  # pro další řádky
            countries = row[i].split('/')
            for country in countries:
                country_name = country.strip()
                country_set = Country.objects.filter(name=country_name)
                if not country_set:
                    Country.objects.create(
                        name=country_name
                    )
                    print(f"Do tabulky Coutry vložena nová země '{country_name}'")
                    new_countries += 1
                else:
                    print(f"Nalezená země '{country_name}' je již v databázi.")

    print(f"Konec skriptu '03_add_countries', bylo přidáno {new_countries} nových zemí.")
