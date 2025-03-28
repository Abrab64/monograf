![MONOGRAF logo](https://monograf.jezik.hr/assets/images/logo-monograf.svg)

![NextGenerationEU logo](https://monograf.jezik.hr/assets/images/logo-nextgen.svg)

# Grafematička korpusna pretraga

**Grafematička korpusna pretraga** je internetski alat za istraživanje povijesnih grafematskih inačica hrvatskih riječi, razvijen u sklopu projekta **Razvoj i primjena modela za normalizaciju grafije starih latiničnih tiskanih tekstova (MONOGRAF)** Instituta za hrvatski jezik. Projekt financira Europska unija – **NextGenerationEU** u okviru **Nacionalnoga plana oporavka i otpornosti** te se provodi od 1. siječnja 2024. do 31. prosinca 2027. Voditelj projekta je **dr. sc. Vuk-Tadija Barbarić**, a suradnic...

> ℹ️ **Napomena**: Ovo je probna aplikacija koja omogućuje pretraživanje **samo jednog teksta** – propovjednog zbornika **Predike** (Venecija, 1742.) autora **Josipa Banovca**, hrvatskog franjevca i propovjednika. Tekst je grafijski vrlo raznolik i vrijedan za istraživanje povijesne hrvatske ortografije.

## 🚀 Mogućnosti

- Unos standardnih hrvatskih riječi (npr. *življenje*, *kršćanin*)
- Automatsko pronalaženje svih povijesnih grafematskih inačica u korpusu
- Isticanje rezultata u obliku KWIC (ključna riječ u kontekstu)
- Podrška za parcijalna podudaranja i grafematsku složenost (npr. *gli*, *gni*, *ſ*, *ç*)
- Jednostavno proširiv za druga grafematska pravila

## 🌍 Kako koristiti

Aplikacija je dostupna putem preglednika na sljedećoj adresi:

👉 **[https://monograf.jezik.hr/pretraga](https://monograf.jezik.hr/pretraga)**

Nije potrebna instalacija ni registracija. Samo unesite riječ i pretražujte grafematske inačice iz korpusa.

## 📁 Struktura datoteka

- `app.py`: Streamlit sučelje
- `search_corpus.py`: Jezgra logike pretraživanja s grafematskim mapiranjem
- `corpus.txt`: Pretraživi korpus
- `requirements.txt`: Python ovisnosti

## 🌐 Kontekst projekta

Ovaj alat razvijen je u okviru projekta **Razvoj i primjena modela za normalizaciju grafije starih latiničnih tiskanih tekstova (MONOGRAF)** – [monograf.jezik.hr](https://monograf.jezik.hr) – koji se provodi u okviru Nacionalnog plana oporavka i otpornosti Republike Hrvatske 2021. – 2026. i financira sredstvima Europske unije iz Instrumenta za oporavak i otpornost u okviru programa **NextGenerationEU**. Projekt ima za cilj digitalnu transformaciju i razvoj računalnih alata za proučavanje hrvatskoga jezik...

Više informacija dostupno je na [monograf.jezik.hr](https://monograf.jezik.hr).

## 🧠 Licenca

Ovaj repozitorij licenciran je pod Creative Commons **Imenovanje-Nekomercijalno 4.0 međunarodna (CC BY-NC 4.0)** licencom.

Slobodno možete:
- **Dijeliti** — kopirati i redistribuirati materijal u bilo kojem mediju ili formatu
- **Prilagoditi** — remiksirati, transformirati i graditi na materijalu

Pod sljedećim uvjetima:
- **Imenovanje** — Morate navesti odgovarajuće autorstvo.
- **Nekomercijalno** — Ne smijete koristiti materijal u komercijalne svrhe.

Puni detalji licence: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

---

![MONOGRAF logo](https://monograf.jezik.hr/assets/images/logo-monograf.svg)

![NextGenerationEU logo](https://monograf.jezik.hr/assets/images/logo-nextgen.svg)

# Graphematic Corpus Search

**Graphematic Corpus Search** is a web-based tool for exploring historical graphematic variants of Croatian words, developed as part of the project **Razvoj i primjena modela za normalizaciju grafije starih latiničnih tiskanih tekstova (MONOGRAF)** by the Institute of Croatian Language. The project is funded by the European Union – **NextGenerationEU** within the **National Recovery and Resilience Plan** of the Republic of Croatia and runs from 1 January 2024 to 31 December 2027. The project is led by **...

> ℹ️ **Note**: This is a prototype application currently supporting search in only one text — the 1742 Venetian sermon collection **Predike** by **Josip Banovac**, a Croatian Franciscan and preacher. The text is notable for its diverse orthography and is a valuable resource for historical linguistics.

## 🚀 Features

- Enter standard Croatian words (e.g., *življenje*, *kršćanin*)
- Automatically finds all historical graphematic variants in the corpus
- Highlights search results in KWIC (Keyword in Context) format
- Supports partial matches and graphematic complexity (e.g. *gli*, *gni*, *ſ*, *ç*)
- Easily extensible for other graphematic rules

## 🌍 How to Use

This tool is available directly via your browser:

👉 **[https://monograf.jezik.hr/pretraga](https://monograf.jezik.hr/pretraga)**

No installation or login required. Just enter a word and explore graphematic variants in the corpus.

## 📁 File Structure

- `app.py`: Streamlit web interface
- `search_corpus.py`: Core search logic with graphematic mapping
- `corpus.txt`: Your searchable corpus text file
- `requirements.txt`: Python dependencies

## 🌐 Project Context

This tool was developed as part of the project **Razvoj i primjena modela za normalizaciju grafije starih latiničnih tiskanih tekstova (MONOGRAF)** – [monograf.jezik.hr](https://monograf.jezik.hr) – implemented within the National Recovery and Resilience Plan of the Republic of Croatia 2021–2026, and funded by the European Union under the **NextGenerationEU** instrument. The project aims to advance the digital transformation of Croatian humanities by developing computational tools for the analysis of his...

Visit [monograf.jezik.hr](https://monograf.jezik.hr) for more information.

## 🧠 License

This repository is licensed under the Creative Commons **Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit.
- **NonCommercial** — You may not use the material for commercial purposes.

Full license details: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
