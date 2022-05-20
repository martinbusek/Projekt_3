import bs4
import requests
import sys
import csv

def main():
    kontrola_argumentu()
    uzemni_celek = sys.argv[1]
    vystupni_soubor = sys.argv[2]

    getr = requests.get(uzemni_celek)
    soup = bs4.BeautifulSoup(getr.text, 'html.parser')
    print(f"Stahuji data z vybraného URL {uzemni_celek}")

    header = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]
    for strana in politicke_strany():
        header.append(strana)

    with open(vystupni_soubor, "w", newline="") as file:
        file_write = csv.writer(file)
        file_write.writerow(header)

        c = cisla_obci(soup)
        n = nazev_obci(soup)
        volici_v_seznamu = loop_obci(link_obci(soup))[0]
        vydane_obalky = loop_obci(link_obci(soup))[0]
        platne_hlasy = loop_obci(link_obci(soup))[0]
        l = loop_obci(link_obci(soup))[1]
        i = 0
        for radek in range(len(link_obci(soup))):
            vlozitradek = []
            vlozitradek.append(c[radek])
            vlozitradek.append(n[radek])
            vlozitradek.append(volici_v_seznamu[radek][0])
            vlozitradek.append(vydane_obalky[radek][1])
            vlozitradek.append(platne_hlasy[radek][2])
            vlozitradek.extend(l[radek])
            file_write.writerow(vlozitradek)

    print(f"Ukládám do souboru {vystupni_soubor}")
    print("Ukončuji scraper")


# Vrátí list všech obcí
def nazev_obci(soup):
    list_obci = []
    for obec in soup.find_all('td', {'class': 'overflow_name'}):
        list_obci.append(obec.text)
    return list_obci

# Vrátí list čísel obcí
def cisla_obci(soup):
    list_cisel = []
    for cisla in soup.find_all('td', {'class': 'cislo'}):
        for a in cisla.find_all('a'):
            list_cisel.append(a.text)
    return list_cisel

# Vrátí list linků všech obcí
def link_obci(soup):
    list_linky = []
    for cislo in soup.find_all('td', {'class': 'cislo'}):
        for a in cislo.find_all('a'):
            list_linky.append("https://volby.cz/pls/ps2017nss/" + a['href'])
    return list_linky

# Loop všemi obcemi, vrátí dva listy
def loop_obci(url):
    list_data = []
    list_hlasu_stran = []
    for i in url:
        obec_response = requests.get(i)
        soup2 = bs4.BeautifulSoup(obec_response.text, "html.parser")
        list_data.append(data_obci(soup2))
        list_hlasu_stran.append(hlasy_stran_obce(soup2))

    return list_data, list_hlasu_stran

# Vrátí list dat z obce (voliči, obálky atp.)
def data_obci(soup2):
    volici_v_seznamu = soup2.find('td', {'headers': 'sa2'}).text
    vydane_obalky = soup2.find('td', {'headers': 'sa3'}).text
    platne_hlasy = soup2.find('td', {'headers': 'sa6'}).text

    return volici_v_seznamu, vydane_obalky, platne_hlasy

# Vrátí list počtů hlasů jednotlivých stran
def hlasy_stran_obce(soup2):
    hlasy_stran = []

    hlasy_1 = soup2.find_all('td', {'headers': 't1sa2 t1sb3'})
    hlasy_2 = soup2.find_all('td', {'headers': 't2sa2 t2sb3'})
    for hlasy in hlasy_1:
        hlasy_stran.append(hlasy.text)
    for hlasy in hlasy_2:
        hlasy_stran.append(hlasy.text)

    return hlasy_stran

# Vrátí list všech stran (hledají se v náhodném odkazu města)
def politicke_strany():
    strany_req = requests.get("https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=8&xobec=572136&xvyber=5202")
    soup_strany = bs4.BeautifulSoup(strany_req.text, "html.parser")
    list_stran = []
    for strany in soup_strany.find_all('td', {'class': 'overflow_name'}):
        list_stran.append(strany.text)

    return list_stran

def kontrola_argumentu():
    if len(sys.argv) != 3:
        print("Špatný počet argumentů")
        quit()
    if "https://volby.cz/pls/ps2017nss/" not in sys.argv[1]:
        print("URL v argumentu není validní")
        quit()
    if ".csv" not in sys.argv[2]:
        print("Výstupní soubor není validní")
        quit()
    else:
        return True

if __name__ == "__main__":
    main()