"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Petra Šnajdrová
email: petrasnajdrova@seznam.cz
"""

import requests
import sys
from bs4 import BeautifulSoup
import csv
from typing import List, Dict

def ziskej_odkazy_na_obce(url: str) -> List[str]:
    """
    Načte odkazy na jednotlivé obce z dané stránky okresu.

    Args:
        url (str): URL adresa okresu

    Returns:
        List[str]: Seznam URL adres pro jednotlivé obce
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    base = "https://www.volby.cz/pls/ps2017nss/"
    odkazy = [base + a["href"] for a in soup.select("td.cislo a")]
    return odkazy

def zpracuj_obec(url: str) -> Dict[str, str]:
    """
    Získá data z konkrétní stránky obce.

    Args:
        url (str): URL adresa konkrétní obce

    Returns:
        Dict[str, str]: Slovník s daty o volbách a hlasy pro strany
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    kod_obce = url.split("xobec=")[1].split("&")[0]
    h3 = soup.find_all("h3")
    nazev_obce = h3[2].get_text(strip=True).replace("Obec: ", "") if len(h3) >= 3 else "Neznámá obec"

    cisla = soup.select("table#ps311_t1 td.cislo")
    volici = cisla[3].text.strip().replace("\xa0", "").replace(" ", "")
    obalky = cisla[4].text.strip().replace("\xa0", "").replace(" ", "")
    platne = cisla[7].text.strip().replace("\xa0", "").replace(" ", "")

    strany = {}
    for table in soup.select("div.t2_470 table"):
        for row in table.find_all("tr")[2:]:
            cells = row.find_all("td")
            if len(cells) >= 3:
                nazev = cells[1].get_text(strip=True)
                hlasy = cells[2].get_text(strip=True).replace("\xa0", "").replace(" ", "")
                strany[nazev] = hlasy

    return {
        "kód_obce": kod_obce,
        "název_obce": nazev_obce,
        "voliči_v_seznamu": volici,
        "vydané_obálky": obalky,
        "platné_hlasy": platne,
        **strany
    }

def uloz_do_csv(vysledky: List[Dict[str, str]], soubor: str) -> None:
    """
    Uloží výsledky do CSV souboru s dynamickými sloupci pro strany.

    Args:
        vysledky (List[Dict[str, str]]): Seznam výsledků pro obce
        soubor (str): Název výstupního souboru
    """
    if not vysledky:
        print("Žádná data k uložení.")
        return

    hlavicky = list(vysledky[0].keys())
    for radek in vysledky[1:]:
        for klic in radek.keys():
            if klic not in hlavicky:
                hlavicky.append(klic)

    with open(soubor, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=hlavicky)
        writer.writeheader()
        writer.writerows(vysledky)

def main() -> None:
    """
    Spustí hlavní proces: validace vstupních argumentů, stažení a uložení dat.
    """
    if len(sys.argv) != 3:
        print("Použití: python main.py <URL_uzemniho_celku> <vystup.csv>")
        return

    url = sys.argv[1]
    vystup = sys.argv[2]

    if "ps32" not in url:
        print("Zadej URL na stránku výběru obcí (např. okres Benešov).")
        return

    odkazy = ziskej_odkazy_na_obce(url)
    print(f"Nalezeno {len(odkazy)} obcí.")

    vysledky = []
    for obec_url in odkazy:
        print(f"Zpracovávám obec: {obec_url}")
        vysledky.append(zpracuj_obec(obec_url))

    uloz_do_csv(vysledky, vystup)
    print(f"Výsledky uloženy do souboru {vystup}")

if __name__ == "__main__":
    main()