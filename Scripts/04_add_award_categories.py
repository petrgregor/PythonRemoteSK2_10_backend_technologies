from django.db import models
from viewer.models import *
import csv
import time
import re

def run():
    AwardCategory.objects.all().delete()
    new_award_categories = 0
    i = 7

    with open('data/Staff.csv', encoding="UTF-8") as file:
        reader = csv.reader(file, delimiter=';')  # otevřeme csv soubor

        header = next(reader)  # první řádek je hlavička tabulky
        print(header)

        for row in reader:  # pro další řádky
            awards = row[i].split('|')
            for award in awards:
                #print(award)
                try:
                    award_category = re.search(r'- (.*?)\)', award).group(1)
                    #print(award_category)
                    award_category_set = AwardCategory.objects.filter(name=award_category)
                    if not award_category_set:
                        AwardCategory.objects.create(
                            name=award_category
                        )
                        print(f"Do tabulky AwardCategory vložena nová kategore '{award_category}'")
                        new_award_categories += 1
                    else:
                        print(f"Nalezená kategorie ocenění '{award_category}' je již v databázi.")
                except:
                    pass

    print(f"Konec skriptu '04_add_award_categories', bylo přidáno {new_award_categories} nových kategorií.")
