from collections import defaultdict
from modules.db_connector import db_connector

db_connector.check_connection()

from modules.io_manager import (display_page_by_page, display_page, input_category, input_year_range, display_selected_category,
                                print_color, input_color, show_statistics, check_for_exit)
from modules.log_manager import (show_popular_keyword, show_popular_category, get_popular,
                                 get_last_uniq, get_last_keyword, get_last_category)

from modules.db_request import (select_all_category, select_by_category_cols, select_by_category_body,
                                select_by_title_cols, select_by_title_body)
from modules.parm_const import (MENU, SEARCH_TYPE, COL_CATEGORY_ID, COL_CATEGORY, COL_YEAR_MIN, COL_YEAR_MAX,
                                KEY_RETURN, TXT_RETURN, KEY_EXIT, MAIN_MENU_TITLE, Q_SEARCH_KEYWORD,
                                COL_KEYWORD_MONGO, BEGIN_MSG_STATISTICS, COLOR_ITEM_MENU, COLOR_RESET)

def find_title(menu: tuple, func_name: str) -> str | None:
    """
    Возвращает title пункта, у которого func == func_name.
    Работает с любой вложенностью подменю.
    """
    for item in menu:
        if item.get("func") == func_name:          # нашли — вернули
            return item["title"]

        # рекурсивно смотрим подпункты
        if "submenu" in item:
            title = find_title(item["submenu"], func_name)
            if title:
                return title
    return None

def search_by_title():
    """ Команда поиска по ключевому слову в названии фильма """

    while True:
        msg = f"{Q_SEARCH_KEYWORD} ([Enter] - {KEY_RETURN[1]}) {COL_KEYWORD_MONGO[2]}"
        keyword = input_color(msg, "Cyan").strip().upper()

        # check_for_exit(keyword)

        if not keyword or keyword.isspace():
            return None

        # находим общее количество совпавших фильмов
        # хотя по умолчанию MySQL не учитывает регистр и в БД "sakila" названия фильмов записаны полностью в верхнем регистре,
        # на всякий случай приведём к одному регистру, завтра могут появиться другие данные или изменятся настройки ядра БД
        select_parm = (f"%{keyword}%",)
        msg_search = f"Suche nach {COL_KEYWORD_MONGO[1]} {COL_KEYWORD_MONGO[2]}'{keyword}'"
        row_cnt = display_page_by_page(select_by_title_cols, select_by_title_body, select_parm, msg_search, keyword)
        if row_cnt:  # записываем в историю поиска
            param = {SEARCH_TYPE[0]: keyword}
            db_connector.insert_log(SEARCH_TYPE[0], param, row_cnt)

            return


def search_by_category():
    """ Команда поиска по жанру и годам (мин-макс) выпуска фильма """

    categories = db_connector.query_execute(select_all_category, fetch="all")
    # вывод результата в таблицу
    print_color("[Liste der gefundenen Genres]", "yellow", True, False)
    # добавляем колонки в таблицу кроме последней (category_id нужна для быстрого поиска, что бы не делать 3-й JOIN)
    cols = ["№"]
    cols.extend(list(categories[0])[:-1])
    # добавляю строки в таблицу (кроме category_id)
    rows = [[i] + [item[col] for col in cols[1:]] for i, item in enumerate(categories, 1)]

    display_page(cols, rows, 1, 1, False)

    category_selected = input_category(categories)
    if not category_selected:
        return

    search_parm = defaultdict()
    search_parm[COL_CATEGORY_ID] = category_selected[COL_CATEGORY_ID]
    search_parm[COL_CATEGORY] = category_selected[COL_CATEGORY]
    year_min, year_max = category_selected[COL_YEAR_MIN], category_selected[COL_YEAR_MAX]
    display_selected_category(search_parm)

    if not input_year_range(search_parm, year_min, year_max):
        return

    row_cnt = display_by_category(search_parm, False)
    if row_cnt:  # записываем в историю поиска
        param = {
            "genre_name": search_parm[COL_CATEGORY],
            "year_start": search_parm["year_start"],
            "year_stop": search_parm["year_stop"]
        }
        db_connector.insert_log(SEARCH_TYPE[1], param, row_cnt)


def display_by_category(search_parm: dict, print_run: bool = True):
    """
    функция вывода найденных по жанру и годам фильмов
    :param search_parm: словарь с выбранными параметрами
                        {category_id': 2, 'гория': 'Animation', 'year_start': 1990, 'year_stop': 2025}
    :param print_run: True - печатать строку с выбранными параметрами
    :return:
    """

    select_parm = (search_parm[COL_CATEGORY_ID], search_parm["year_start"], search_parm["year_stop"])
    msg_search = display_selected_category(search_parm, print_run)

    return display_page_by_page(select_by_category_cols, select_by_category_body, select_parm, msg_search)


def print_title_statistics(menu_item_func):
    """
    Функция определяет пункт вызванный пункт меню Статистики.
    Возвращает название пункта меню без первого слова BEGIN_MSG_STATISTICS ("Посмотреть")
    :return: в строке название выбранной статистики
    """
    # используем итератор чтобы по ключу "menu_func" найти название пункта меню (ключ "name")
    ##title = next(item["name"] for item in MENU if item["submenu"] == menu_item_func)
    # удаляем первое слово BEGIN_MSG_STATISTICS ("Посмотреть")
    title = find_title(MENU, menu_item_func)
    title = title.replace(BEGIN_MSG_STATISTICS, "", 1).strip()
    print_color(f"[{title}]", "yellow", True, False)

    return None


def show_popular_query():
    """
    команда вывода статистики популярных запросов
    """
    print_title_statistics("show_popular_query")
    # tabl_keyword = show_popular_keyword()
    # tabl_category = show_popular_category()
    # tabl_popular = combined_lists(tabl_keyword, tabl_category)  # склеим две таблицы
    tabl_popular = get_popular()
    show_statistics(tabl_popular)

    return None


def show_popular_query_full():
    """
    команда вывода статистики популярных запросов отдельно по ключевому слову и отдельно по категории+годам
    """
    print_title_statistics("show_popular_query_full")
    tabl_keyword = show_popular_keyword()
    tabl_category = show_popular_category()

    show_statistics(tabl_keyword, tabl_category)

    return None


def show_last_query():
    """
    команда вывода статистики последних запросов
    """
    print_title_statistics("show_last_query")
    #tabl_last = show_last()
    tabl_last = get_last_uniq()
    show_statistics(tabl_last)

    return None


def show_last_query_full():
    """
    команда вывода статистики последних запросов отдельно по ключевому слову и отдельно по категории+годам
    """
    print_title_statistics("show_last_query_full")
    # tabl_keyword = show_last_keyword()
    #tabl_category = show_last_category()
    tabl_keyword = get_last_keyword()
    tabl_category = get_last_category()

    show_statistics(tabl_keyword, tabl_category)

    return None

MENU_FUNCTIONS = {
    f.__name__: f for f in (
        search_by_title, search_by_category,
        show_popular_query, show_last_query,
        show_popular_query_full, show_last_query_full
    )}


class MenuManager:
    """
    Менеджер меню
    """
    EXIT = 0

    def __init__(self, menu_cfg: tuple[dict], title: str=MAIN_MENU_TITLE):
        self.title = f" [{title}] "
        self.menu_cfg = menu_cfg  # текущий уровень меню
        if title == MAIN_MENU_TITLE:
            self.main = True
        else:
            self.main = False

    def display(self):
        """
        показ нумерованного меню
        :return:
        """
        max_len_title = max(len(f"{i}. {item['title']}") for i, item in enumerate(self.menu_cfg, 1))
        if max_len_title > len(self.title):
            line = self.title.center(max_len_title, "-")
        else:
            line = self.title
        print_color(f"{line}", "yellow", True, False)
        for i, item in enumerate(self.menu_cfg, 1):
            msg = f"{COLOR_ITEM_MENU}{i}{COLOR_RESET}. {item['title']}"
            print(msg)
        print("-" * max_len_title)
        if  self.main:
            msg = f"{COLOR_ITEM_MENU}{KEY_EXIT[0]}{COLOR_RESET} - {KEY_EXIT[1]}"
            print(msg, "\n")
        else:
            msg = f"{TXT_RETURN} / [{KEY_EXIT[0]}] - {KEY_EXIT[1]}"
            print_color(msg, "Blue", False)


    def run(self):
        """
        главный цикл выбранного меню
        :return:
        """
        while True:
            self.display()
            choice = self._get_choice()
            if choice == self.EXIT:
                break

            item = self.menu_cfg[choice - 1]

            # если у пункта есть подменю – рекурсивно запускаем новый менеджер
            if "submenu" in item:
                submenu = MenuManager(item["submenu"], title=item["title"])
                submenu.run()
            else:
                self._execute(item["func"])

    def _get_choice(self):
        """
        ввод и валидация пункта
        :return:
        """
        while True:
            num = input("Wählen Sie den Punkt --> ").strip()
            check_for_exit(num,  self.main)
            if num.isdigit():
                num = int(num)
                if 0 <= num <= len(self.menu_cfg):
                    return num
            msg_error_num = f"⛔ 2 Sie die richtige Nummer des Punktes an. Verfügbare Werte von 0 bis {len(self.menu_cfg)}!"
            print(msg_error_num)

    def _execute(self, func_name):
        """
        вызов функции по имени
        :param func_name:
        :return:
        """
        func = MENU_FUNCTIONS.get(func_name)
        if callable(func):
            func()
        else:
            print(f"⚠️ Die Funktion '{func_name}' wurde nicht gefunden.")

    def get_title(self):
        return self.title


if __name__ == "__main__":

    MenuManager(MENU, MAIN_MENU_TITLE).run()

    print("Tschüss 👋")
