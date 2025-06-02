# Projekt_3
Tento script slouží ke stažení a uložení volebních výsledků z voleb do Poslanecké sněmovny 2017 z webu [volby.cz](https://www.volby.cz). Výsledky jsou ukládány do CSV souboru.

## 📦 Instalace
Nejdříve je doporučeno vytvořit a aktivovat virtuální prostředí:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
```

### Potřebné knihovny
Seznam potřebných knihoven je uveden v souboru `requirements.txt` a pro jejich instalaci následujte níže uvedený postup:
```bash
pip install -r requirements.txt
```

## 🚀 Použití

Skript se spouští z příkazového řádku s těmito dvěma argumenty:

```bash
python main.py <URL_na_okresní_stránku_z_volby.cz> <název_výstupního_souboru.csv>
```

### Příklad:

Pro získání výsledků pro okres Benešov:

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky_benesov.csv
```

## 📄 Výstupní CSV formát

CSV soubor obsahuje následující sloupce:

- `kód_obce`
- `název_obce`
- `voliči_v_seznamu`
- `vydané_obálky`
- `platné_hlasy`
- Jednotlivé sloupce pro každou **kandidující stranu** s počtem hlasů

## 🛠 Poznámky

- Skript nepočítá se zahraničím (nejsou zahrnuty v odkazech).
- Zpracovává všechny obce zadaného okresu.
- Skript je testován pro stránky z volební databáze ČSÚ pro rok 2017.

---
Tento projekt vznikl jako výukové cvičení na téma web scraping v Pythonu.
