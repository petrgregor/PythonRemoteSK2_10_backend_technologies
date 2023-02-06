# Hollymovies project

Aplikace pro práci s filmovou databází.

Hlavní funkce:
- ✓ výpis všech filmů v databázi
- ✓ filtrování filmů dle žánru
- ✓ filtrování filmů dle hodnocení
- ✓ filtrování podle herce
- ✓ filtrování podle režiséra
- ✓ filtrování podle klíčového slova
- ✓ vyhledávání
- žebříčky (dle hodnocení filmu)
- žebříčky uživatelů (nejaktivnější,...)
- oblíbené filmy
- ✓ poslední navštívené
- ✓ novinky
- ✓ výběr náhodného filmu
- ✓ registrace a login uživatelů
  - ✓ hodnocení filmů
  - komentáře k filmům + editace
  - ✓ možnost vložit nový film
  - ✓ možnost editace filmu
  - ✓ možnost mazání filmu
  - statistiky uživatelů (kolik hodnotili filmů, průměrné hodnocení,...)
  - (ne)viděl jsem
  - seznam, co chce uživatel vidět
  - zpráva adminovi (chat)
- reklamní banner 
- predikce oblíbenosti filmu
- podobné filmy (dle žánru a hodnocení)
- link na sociální sítě
- ✓ API
- ✓ PostgreSQL databáze
- upravit CSS
- testování

Databáze:
- Movie 
  - Title
  - Title_orig
  - Title_sk
  - Země výroby
  - Žánr
  - Datum premiéry
  - Režisér
  - Herci
  - Délka filmu
  - Popis
  - Náklady
  - Výdělek
  - Přístupnost
  - Fotografie / cover
  - ukázky / trailery
  - Průměr hodnocení - vypočítá z tabulky hodnocení (1-5 hvězd)
  - Cena za přehrání
  - Odkaz na přehrání
  - kategorie ?
- Genre
  - name
- Users - už hotovo (je přímo v Django)
- Staff
  - jméno
  - příjmení
  - země
  - datum narození
  - datum úmrtí
  - biografie
  - ocenění
  - galerie
 