# 🎬 Filmsuche (Final Project)

Ein Python-Konsolenprogramm, das Filme in der MySQL-Datenbank **Sakila** sucht, alle Anfragen in MongoDB protokolliert  
und Statistiken zu den beliebtesten oder letzten Suchanfragen anzeigt.

---

## Möglichkeiten

| Funktion                           | Beschreibung                                                                                                                                                                                                        |
|------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Suche nach  Schlüsselwort**         | ‑ sucht nach einem  Treffer im Filmtitel;<br>‑ Die Ergebnisse werden in 10 Filmen mit vollständiger Seiten-Navigation angezeigt.;                                                                                   |
| **Suche nach  Genre + Jahrgänge** | ‑ Vor der Anfrage wird eine Liste der Genres und des  minimalen/maximalen Jahres aus der Datenbank angezeigt;<br>‑ Der Benutzer legt die Grenzen fest, z. B. *2005–2012* oder *2005–2005*;<br>‑ 10 Filme pro Seite; |
| **Logging**                    | Jede erfolgreiche Anfrage wird in der Kollektion `MONGO_COLLECTION` (MongoDB) gespeichert;                                                                                                                          |
| **Statistik**                     | Der Befehl „Beliebte oder letzte Suchanfragen“ zeigt die Top 5 nach Häufigkeit (oder die letzten 5) usw. an;                                                                                                                        |

---

## Technologie-Stack

* **Python 3.9+**
* **MySQL** — Quelle für Filmdaten  
  (Getestet auf der Demo-Datenbank *Sakila*)
* **MongoDB** — Speicherung des Anfrageverlaufs
* Bibliotheken: `pymysql`, `pymongo`, `rich`, `prettytable` 

---

## Installation

```bash
git clone https://github.com/<your‑repo>/movie_search.git
cd movie_search
python -m venv venv
source venv/bin/activate         # Windows → venv\Scripts\activate
pip install -r requirements.txt

python main.py

----------------------- Hauptmenü -----------------------
1. Suche nach Filmtitel.
2. Suche nach Genre und Ausgabejahr.
3. Statistik der Anfragen.
--------------------------------------------------------------
0 - schließen

Выберите: 

.
├─ main.py            # Einstiegspunkt, Menü
├─ .env.example       # Umgebungvariable Vorlage
├─ README.md
├─ tests.py.py        # Tests (in Entwicklung)
└─ modules            # Module
  ├─ parm_const.py    # Das Menüinhalt, die Namen der Spalten in den Tabellen, die Anzahl der Zeilen pro Seite usw. sind festgelegt.
  ├─ db_connector.py  # Verbindung zu MySQL und MongoDB, Ausführung von SQL-Abfragen, Schreiben/Lesen in MongoDB
  ├─ db_request.py    # SQL-Anfragen
  ├─ log_manager.py   # Anfragen in MongoDB – Auswahl von Statistiken
  └─ io_manager.py    # Eingabe-/Ausgabefunktionen (Farbeneingabe/-ausgabe, Blättern in Tabellen...)

```
__Einstellung der Benutzeroberfläche__ 
``` 
In der Datei „parm_const.py” ist Folgendes angegeben:
  - Menüinhalt; 
  - Menüpunkte [kann in jeder Sprache geschrieben werden]; 
  - Namen der Spalten in Tabellen [können in jeder Sprache geschrieben werden];
  - Farbe der Tabellenspalten;
  - Farbe der Hervorhebung des gefundenen Schlüsselworts im Filmtitel;
  - Anzahl der Zeilen pro Seite; 
  - Anzahl der Zeilen der Bewertung;
  ...
```
__Beispiele für die Arbeit mit dem Konsolenprogramm__ 
```
$ python main.py

Введите ключевое слово для поиска в названии (Enter - назад, . - выход) 🔑: ame

Поиск по ключевому слову 🔑'DA'

Найдено фильмов: 55   (Всего страниц: 6)
+----+----------------------+-------------+
| №  | Название фильма      | Год выпуска |
+----+----------------------+-------------+
| 1  | ADAPTATION HOLES     |     2018    |
| 2  | ALADDIN CALENDAR     |     2008    |
...0
| 10 | CAUSE DATE           |     2022    |
+----+----------------------+-------------+
--- Страница 1 из 2 ---
Навигация: + -след. / # -номер_страницы / 0 - назад / . - выход: 

$ python main.py

Список найденных жанров
+----+-------------+----------------------+-----------------------+----------------+
| №  | Жанр        | Минимальный год вып. | Максимальный год вып. | Кол-во фильмов |
+----+-------------+----------------------+-----------------------+----------------+
| 1  | Action      |         1990         |          2025         |       64       |
| 2  | Animation   |         1990         |          2025         |       66       |
...
| 16 | Travel      |         1990         |          2025         |       57       |
+----+-------------+----------------------+-----------------------+----------------+0
Введите Номер / Название жанра из списка (0 - назад, . - выход): 12

Вы выбрали Жанр 'Music'
Укажите Минимальный год выпуска.
Доступные значения: 1990 - 2025 (Enter - 1990, 0 - назад, . - выход) -->: 1993
Вы выбрали Жанр 'Music', год с 1993
Укажите Максимальный год выпуска.
Доступные значения: 1993 - 2025 (Enter - 2025, 0 - назад, . - выход) -->: 2000

Вы выбрали Жанр 'Music', год с 1993 по 2000
Найдено фильмов: 15   (Всего страниц: 2)
+----+---------------------+-------------+
| №  | Название фильма     | Год выпуска |
+----+---------------------+-------------+
| 1  | ALASKA PHANTOM      |     2023    |
| 2  | ALONE TRIP          |     2016    |
...
| 10 | CLONES PINOCCHIO    |     1993    |
+----+---------------------+-------------+
--- Страница 1 из 2 ---
Навигация: Enter -след. / # -номер_страницы / 0 - назад / . - выход: 

$ python main.py

--------------------------- Статистика запросов ---------------------------
1. Посмотреть Топ 5 ПОПУЛЯРНЫХ запросов.
2. Посмотреть Топ 5 ПОСЛЕДНИХ уникальных запросов.
3. Посмотреть Топ 5 ПОПУЛЯРНЫХ уник. запросов (по ключевому слову или жанру).
4. Посмотреть Топ 5 ПОСЛЕДНИХ уник. запросов (по ключевому слову или жанру).
-----------------------------------------------------------------------------
0 - назад / . - выход
Выберите: 1

Топ 5 ПОПУЛЯРНЫХ запросов.
+---+----------------+-------------------+-------+--------+-----------------+
| № | Запрос по      | Параметры запроса | Год с | Год по | Кол-во запросов |
+---+----------------+-------------------+-------+--------+-----------------+
| 1 | Ключевое слово | 🔑'AME'           |       |        |        6        |
| 2 | Жанр           | Children          |  1990 |  2025  |        4        |
| 3 | Жанр           | Sci-Fi            |  1990 |  2025  |        3        |
| 4 | Жанр           | Action            |  1990 |  2025  |        2        |
| 5 | Жанр           | Foreign           |  1990 |  2025  |        2        |
+---+----------------+-------------------+-------+--------+-----------------+

Топ 5 ПОПУЛЯРНЫХ уникальных запросов (сводная).
+---+----------------+-----------------+--------+-------------------+-------+--------+------------------+
| № | Ключевое слово | Кол-во запросов |   🤩   | Параметры запроса | Год с | Год по | Кол-во запросов: |
+---+----------------+-----------------+--------+-------------------+-------+--------+------------------+
| 1 | 🔑'AME'        |        6        |  ✯✯✯✯✯ | Children          |  1990 |  2025  |        4         |
| 2 | 🔑'SA'         |        3        |   ✯✯✯✯ | Drama             |  1990 |  2025  |        3         |
| 3 | 🔑'THE'        |        3        |    ✯✯✯ | New               |  1990 |  2025  |        3         |
| 4 | 🔑'AS'         |        2        |     ✯✯ | Sci-Fi            |  1990 |  2025  |        3         |
| 5 | 🔑'SE'         |        2        |      ✯ | Action            |  1990 |  2025  |        2         |
+---+----------------+-----------------+--------+-------------------+-------+--------+------------------+
...