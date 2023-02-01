from django.db import models
from viewer.models import *
import csv
import time
import re

def run():
    new_images = 0
    i = 11

    with open('data/Movies.csv', encoding="UTF-8") as file:
        reader = csv.reader(file, delimiter=';')  # otevřeme csv soubor

        header = next(reader)  # první řádek je hlavička tabulky
        print(header)

        for row in reader:  # pro další řádky
            images = row[i].split('|')
            for image in images:
                image = image.strip()
                #print(image)
                image_set = Image.objects.filter(path=image)
                if not image_set:
                    Image.objects.create(
                        path=image
                    )
                    print(f"Do tabulky Image vložen nový obrázek '{image}'")
                    new_images += 1
                else:
                    print(f"Nalezený obrázek '{image}' je již v databázi.")


    print(f"Konec skriptu '05_add_images', bylo přidáno {new_images} nových obrázků.")
