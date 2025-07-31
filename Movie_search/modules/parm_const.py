PAGE_SIZE = 10  # размер страницы при выводе результатов поиска
TOP_QUERIES = 5
BEGIN_MSG_STATISTICS = "Посмотреть"
MAIN_MENU = (
    {"name": "Поиск по названию фильма.",
     "menu_func": "search_by_title"},
    {"name": "Поиск по жанру и диапазону годов выпуска.",
     "menu_func": "search_by_category"},
    {"name": f"{BEGIN_MSG_STATISTICS} статистику по популярным или последним запросам.",
     "menu_func": "menu_statistics"}
)

MENU_STATISTICS = (
    {"name": f"{BEGIN_MSG_STATISTICS} Топ {TOP_QUERIES} ПОПУЛЯРНЫХ запросов.",
     "menu_func": "show_popular_query"},
    {"name": f"{BEGIN_MSG_STATISTICS} Топ {TOP_QUERIES} ПОСЛЕДНИХ уникальных запросов.",
     "menu_func": "show_last_query"},
    {"name": f"{BEGIN_MSG_STATISTICS} Топ {TOP_QUERIES} ПОПУЛЯРНЫХ уник. запросов (по ключевому слову или жанру).",
     "menu_func": "show_popular_query_full"},
    {"name": f"{BEGIN_MSG_STATISTICS} Топ {TOP_QUERIES} ПОСЛЕДНИХ уник. запросов (по ключевому слову или жанру).",
     "menu_func": "show_last_query_full"}
)

KEY_RETURN = ("0", "назад")
KEY_EXIT = (".", "выход")
TXT_RETURN = f"[{KEY_RETURN[0]}] - {KEY_RETURN[1]}"
TXT_EXIT = f"[{KEY_EXIT[0]}] - {KEY_EXIT[1]}"
SEARCH_TYPE = ("keyword", "category_year")
COL_FILM = "Название фильма"
COL_FILM_YEAR = "Год выпуска"
COL_FILM_CNT = "Кол-во фильмов"
COL_CATEGORY_ID = "category_id"
COL_CATEGORY = "Жанр"
COL_YEAR_MIN = "Минимальный год выпуска"
COL_YEAR_MAX = "Максимальный год выпуска"
COL_SEPARATOR = "  🤩  "
COL_KEYWORD_MONGO = ("keyword", "Ключевое слово", "🔑")
COL_CATEGORY_MONGO = ("genre_name", "Жанр")
COL_YEAR_START_MONGO = ("year_start", "Год с")
COL_YEAR_STOP_MONGO = ("year_stop", "Год по")
COL_CNT_MONGO = ("cnt", "Количество")
COL_CNT_KEYWORD = "cnt_keyword"
COL_CNT_CATEGORY = "cnt_category"
COL_RESULT_COUNT = "results_count"
MONGO_COLS = {"timestamp": "Дата запроса",
              "date": "Дата запроса:",
              "search_type": "Запрос по",
              COL_CATEGORY_MONGO[0]: "Параметры запроса",  # COL_CATEGORY_MONGO[1],
              COL_YEAR_START_MONGO[0]: COL_YEAR_START_MONGO[1],
              COL_YEAR_STOP_MONGO[0]: COL_YEAR_STOP_MONGO[1],
              COL_CNT_KEYWORD: "Кол-во запросов",
              COL_CNT_CATEGORY: "Кол-во запросов:",
              "cnt": "Кол-во запросов",
              "and": COL_SEPARATOR,
              COL_KEYWORD_MONGO[0]: COL_KEYWORD_MONGO[1],
              COL_RESULT_COUNT: "Найдено фильмов",
              "result": "Найдено фильмов:"
              }
CHECK_COL_PARM = {
    COL_KEYWORD_MONGO[0]: COL_CATEGORY_MONGO[0],
    COL_CATEGORY_MONGO[0]: COL_KEYWORD_MONGO[0],
}
