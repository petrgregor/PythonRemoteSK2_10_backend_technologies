from django.db import models
from viewer.models import *
import csv
import time

def run():
    new_age_restrictions = 0
    i = 10

    with open('data/Movies.csv', encoding="UTF-8") as file:
        reader = csv.reader(file, delimiter=';')  # otevřeme csv soubor

        header = next(reader)  # první řádek je hlavička tabulky

        for row in reader:     # pro další řádky
            age_restr = row[i].strip()
            age_restr_set = AgeRestriction.objects.filter(name=age_restr)
            if not age_restr_set:
                AgeRestriction.objects.create(
                    name=age_restr
                )
                print(f"Do tabulky AgeRestriction vložno {age_restr}")
                new_age_restrictions += 1
            else:
                print(f"Nalezené věkové omezení '{age_restr}' je již v databázi.")

    print(f"Konec skriptu '02_add_countries', bylo přidáno {new_age_restrictions} nových zemí.")
