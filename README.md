# Traffic Jam

PyQt6 aplikacija, ki vizualno prikaze zastoj avtov na enopasovni cesti. Simulacija prikaze, kako se vozila postopoma upocasnijo in razporedijo pred ozkim grlom ter kako se promet znova pospesi po izhodu iz zastoja. Animacija temelji na enostavnem modelu odzivov voznika na razdaljo in spremembe hitrosti, zato jasno pokaze nastanek in razsirjanje zastojev.

## Kaj aplikacija prikaze
- rdece obarvano obmocje predstavlja del ceste, kjer se promet upocasni,
- avtomobili med voznjo upostevajo razdaljo do vozila pred seboj in intenziteto zaviranja,
- povprecna hitrost kolone se izpisuje v spodnji vrstici,
- gumbi omogocajo zagon, pavzo in ponastavitev simulacije.

## Delovanje simulacije
- vozila krozijo po virtualni progi dolzine 1200 px, kar predstavlja en pas, ki se zakljuci v zanki,
- med 520 px in 700 px je definiran zastoj, zato vozila v tem obmocju pospeseno upocasnijo,
- hitrost vsakega vozila je omejena z varnostnim razmakom; manj kot je prostora, bolj agresivno zavira,
- deterministicni pospesek in zaviranje (70 px/s^2 oz. 110 px/s^2) zagotavljata gladke prehode,
- povprecna hitrost kolone se pretvori v km/h in prikaze v statusni vrstici.

## Kontrole
- **Start** - sprozi animacijo iz zacetnega pavziranega stanja,
- **Pavza/Nadaljuj** - zacasi simulacijo ali nadaljuje tekoco animacijo,
- **Ponastavi** - ponovno nakljucno razporedi vozila, hkrati pa ohrani trenutno stanje (pavza ali tek).

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

Po zagonu se odpre glavno okno z animacijo prometa. Gumb *Start* najprej sprozi simulacijo, *Pavza* jo ustavi (ponovni klik nadaljuje), *Ponastavi* pa na novo razporedi avtomobile na cesti.

## Struktura projekta
- `main.py` - zacetna tocka aplikacije in logika simulacije,
- `requirements.txt` - seznam potrebnih paketov,
- `README.md` - ta datoteka.

## Workflow
Visok nivo poteka zagona, UI kontrol in simulacijske zanke je prikazan v `workflow.svg`.

## Nadaljnje ideje
- dodajanje drugega pasu ali prehitevanja,
- prikaz grafa hitrosti skozi cas,
- prilagajanje dolzine zastoja in stevila vozil preko vmesnika.
