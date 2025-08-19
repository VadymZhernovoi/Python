PAGE_SIZE = 10  # размер страницы при выводе результатов поиска
TOP_QUERIES = 5 # статистика: посмотреть ТОП 5 ...

COLOR_SELECT  = "\033[33m"      # выделять цветом найденные вхождения keyword в названии фильма
COLOR_ITEM_MENU  = "\033[34m"   # выделить цветом номер пункта меню
COLOR_TABLE_COLS  = "\033[34m"  # выделить цветом названия столбцов в таблице
COLOR_RESET = "\033[0m"         # снять выделение

SEARCH_TYPE = ("keyword", "category_year")
COL_FILM = "Filmtitel" # "Название фильма"
COL_FILM_YEAR = "Ausgabejahr" # "Год выпуска"
COL_FILM_CNT = "Anzahl der Filme" # "Кол-во фильмов"
COL_CATEGORY_ID = "category_id"
COL_CATEGORY = "Genre" # "Жанр"
COL_YEAR_MIN = "Min. Ausgabejahr" # "Минимальный год вып."
COL_YEAR_MAX = "Max. Ausgabejahr" # "Максимальный год вып."
COL_SEPARATOR = "  🤩  "
COL_KEYWORD_MONGO = ("keyword", "Schlüsselwort", "🔑") # ("keyword", "Ключевое слово", "🔑")
COL_CATEGORY_MONGO = ("genre_name", COL_CATEGORY)
COL_YEAR_START_MONGO = ("year_start", "Jahr von") # ("year_start", "Год с")
COL_YEAR_STOP_MONGO = ("year_stop", "Jahr bis") # ("year_stop", "Год по")
COL_CNT_MONGO = ("cnt", "Anzahl") # ("cnt", "Количество")
COL_CNT_KEYWORD = "cnt_keyword"
COL_CNT_CATEGORY = "cnt_category"
COL_RESULT_COUNT = "results_count"
COL_DATE_REQUEST = "Anfragezeit" #"Дата запроса"
COL_CNT_REQUEST = "Anzahl der Anfragen" # "Кол-во запросов"
COL_CNT_FOUND = "Filme gefunden" # "Найдено фильмов"
BEGIN_MSG_STATISTICS = "anzeigen" # "Посмотреть"
MAIN_MENU_TITLE = "Hauptmenü"
KEY_RETURN = ("0", "zurück") # ("0", "назад")
KEY_EXIT = (".", "schließen") # (".", "выход")
Q_EXIT = "Möchten Sie das Programm wirklich beenden? ([y] – beenden, [sonst] – bleiben)"
Q_SEARCH_KEYWORD = f"Geben Sie ein [{COL_KEYWORD_MONGO[1]}] für die Suche im Titel ein"
Q_SEARCH_CATEGORY = "Geben Sie die [Nummer] / [Name] des Genres aus der Liste ein"
ERR_SEARCH_CATEGORY = "Keine Angabe Nummer / Name des Genres!" # "Не указан Номер / Название жанра!"
ERR_FORMAT_INP = "Falsches Eingabeformat" # "Неверный формат ввода"
ERR_UNKNOWN = "Etwas ist schief gelaufen:" # "Что-то пошло не так:"
MSG_NOT_FOUND = "Keine Daten gefunden" # "Данных не найдено"
MSG_EXIT = "Vielen Dank für Ihre Aufmerksamkeit! Bis bald."
AVAIL_VALUE = "Verfügbare Werte:" # "Доступные значения:"

MONGO_COLS = {"timestamp": COL_DATE_REQUEST,
              "date": f"{COL_DATE_REQUEST}:",
              "search_type": "Anfrage nach", # "Запрос по",
              COL_CATEGORY_MONGO[0]: "Anfrageparameter", # "Параметры запроса",  # COL_CATEGORY_MONGO[1],
              COL_YEAR_START_MONGO[0]: COL_YEAR_START_MONGO[1],
              COL_YEAR_STOP_MONGO[0]: COL_YEAR_STOP_MONGO[1],
              COL_CNT_KEYWORD: COL_CNT_REQUEST,
              COL_CNT_CATEGORY: f"{COL_CNT_REQUEST}:",
              "cnt": COL_CNT_REQUEST,
              "and": COL_SEPARATOR,
              COL_KEYWORD_MONGO[0]: COL_KEYWORD_MONGO[1],
              COL_RESULT_COUNT: COL_CNT_FOUND,
              "result": f"{COL_CNT_FOUND}:"
              }
TXT_RETURN = f"[{KEY_RETURN[0]}] - {KEY_RETURN[1]}"
TXT_EXIT = f"[{KEY_EXIT[0]}] - {KEY_EXIT[1]}"

CHECK_COL_PARM = {
    COL_KEYWORD_MONGO[0]: COL_CATEGORY_MONGO[0],
    COL_CATEGORY_MONGO[0]: COL_KEYWORD_MONGO[0],
}
# ─────────────────────────  Конфигурация меню  ────────────────────
MENU = (
    {"title": f"Suche nach {COL_KEYWORD_MONGO[1]}",             "func": "search_by_title"},
    {"title": f"Suche nach {COL_CATEGORY} und {COL_FILM_YEAR}",  "func": "search_by_category"},
    {"title": "Statistik der Anfragen",                 # ← подменю
     "submenu": (
         {"title": f"TOP {TOP_QUERIES} die beliebtesten einzigartigen Anfragen {BEGIN_MSG_STATISTICS}",
          "func": "show_popular_query"},
         {"title": f"TOP {TOP_QUERIES} die letzten einzigartigen Anfragen {BEGIN_MSG_STATISTICS}",
          "func": "show_last_query"},
         {"title": f"TOP {TOP_QUERIES} die beliebtesten einzigartigen Anfragen (zusammengefasst) {BEGIN_MSG_STATISTICS}",
          "func": "show_popular_query_full"},
         {"title": f"TOP {TOP_QUERIES} die letzten einzigartigen Anfragen (zusammengefasst) {BEGIN_MSG_STATISTICS}",
          "func": "show_last_query_full"},
     )},
)
# MENU = (
#     {"title": "Поиск по ключевому слову",            "func": "search_by_title"},
#     {"title": "Поиск по жанру и диапазону лет",      "func": "search_by_category"},
#     {"title": "Статистика запросов",                 # ← подменю
#      "submenu": (
#          {"title": f"{BEGIN_MSG_STATISTICS} Топ {TOP_QUERIES} популярных запросов",
#           "func": "show_popular_query"},
#          {"title": f"{BEGIN_MSG_STATISTICS} Топ {TOP_QUERIES} последних уникальных запросов",
#           "func": "show_last_query"},
#          {"title": f"{BEGIN_MSG_STATISTICS} Топ {TOP_QUERIES} популярных уникальных (сводная)",
#           "func": "show_popular_query_full"},
#          {"title": f"{BEGIN_MSG_STATISTICS} Топ {TOP_QUERIES} последних уникальных (сводная)",
#           "func": "show_last_query_full"},
#      )},
# )
# MAIN_MENU = (
#     {"name": "Поиск по названию фильма.",
#      "menu_func": "search_by_title"},
#     {"name": "Поиск по жанру и диапазону годов выпуска.",
#      "menu_func": "search_by_category"},
#     {"name": f"{BEGIN_MSG_STATISTICS} статистику по популярным или последним запросам.",
#      "menu_func": "menu_statistics"}
# )
#
# MENU_STATISTICS = (
#     {"name": f"{BEGIN_MSG_STATISTICS} Топ {TOP_QUERIES} ПОПУЛЯРНЫХ запросов.",
#      "menu_func": "show_popular_query"},
#     {"name": f"{BEGIN_MSG_STATISTICS} Топ {TOP_QUERIES} ПОСЛЕДНИХ уникальных запросов.",
#      "menu_func": "show_last_query"},
#     {"name": f"{BEGIN_MSG_STATISTICS} Топ {TOP_QUERIES} ПОПУЛЯРНЫХ уникальных запросов (сводная).",
#      "menu_func": "show_popular_query_full"},
#     {"name": f"{BEGIN_MSG_STATISTICS} Топ {TOP_QUERIES} ПОСЛЕДНИХ уникальных запросов (сводная).",
#      "menu_func": "show_last_query_full"}
# )