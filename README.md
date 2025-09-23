# Traffic Jam

PyQt6 aplikacija, ki vizualno prikaze zastoj avtov na enopasovni cesti. Simulacija prikaze, kako se vozila postopoma upocasnijo in razporedijo pred ozkim grlom ter kako se promet znova pospesi po izhodu iz zastoja.

## Kaj aplikacija prikaze
- rdece obarvano obmocje predstavlja del ceste, kjer se promet upocasni,
- avtomobili med voznjo upostevajo razdaljo do vozila pred seboj in divjajoce zavore,
- povprecna hitrost kolone se izpisuje v spodnji vrstici,
- gumbi omogocajo pavzo in ponastavitev simulacije.

## Zahteve
- Python 3.10 ali novejsi
- Virtualno okolje je priporocljivo
- Odvisnosti iz `requirements.txt`

## Namestitev
1. Ustvari virtualno okolje (opcijsko):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Namesti odvisnosti:
   ```bash
   pip install -r requirements.txt
   ```

## Zagon
Za zagon simulacije izvedi:
```bash
python main.py
```

Po zagonu se odpre glavno okno z animacijo prometa. Gumb *Pavza* ustavi dogajanje (ponovni klik nadaljuje), *Ponastavi* pa na novo razporedi avtomobile na cesti.

## Struktura projekta
- `main.py` — zacetna tocka aplikacije in logika simulacije,
- `requirements.txt` — seznam potrebnih paketov,
- `README.md` — ta datoteka.

## Nadaljnje ideje
- dodajanje drugega pasu ali prehitevanja,
- prikaz grafa hitrosti skozi cas,
- prilagajanje dolzine zastoja in stevila vozil preko vmesnika.
