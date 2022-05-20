# Elections scraper
Tento program je využíván k extrahování výsledků z parlamentních voleb ze stránky kterou najdete [ZDE](https://volby.cz/).
## Spuštění programu
### Instalace knihoven
Veškeré knihovny a jejich verze jsou uložené v souboru pod jménem ```requirements.txt```. Pro instalaci knihoven spustě následovný kód na místě kde se nachází ```requirements.txt```. <br />
<br />
```$ pip install -r requirements.txt```
### Argumenty
Program vyžaduje dva (2) argumenty a musí být ve správném pořadí <br />
1. První argument: Validní URL adresu (např. "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4202")
2. Druhý argument: Výstupní soubor (např. "vystup.csv")
### Ukázka
```python scraper.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4202' 'vystup.csv'``` <br />
<br />
Soubor ```vystup.csv``` se uloží tam odkud spouštíte program.