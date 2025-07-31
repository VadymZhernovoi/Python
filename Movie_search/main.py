from collections import defaultdict
from modules.db_connector import db_connector

db_connector.check_connection()

from modules.io_manager import (display_page_by_page, display_page, input_year, display_selected_category, print_error,
                                print_color, input_color, show_statistics, check_for_exit)
from modules.log_manager import (show_popular_keyword, show_popular_category, get_popular,
                                 get_last_uniq, get_last_keyword, get_last_category)

from modules.db_request import (select_all_category, select_by_category_cols, select_by_category_body,
                                select_by_title_cols, select_by_title_body)
from modules.parm_const import (MAIN_MENU, MENU_STATISTICS, SEARCH_TYPE, COL_CATEGORY_ID, COL_CATEGORY,
                                COL_YEAR_MIN, COL_YEAR_MAX, KEY_RETURN, TXT_RETURN, KEY_EXIT, TXT_EXIT,
                                COL_KEYWORD_MONGO, BEGIN_MSG_STATISTICS, COLOR_ITEM_MENU, COLOR_RESET)


def form_menu(menu: tuple[dict], title: str = '', main: bool = False):
    """
    Формирует меню
    :param menu: словарь строк меню, содержащий название пункта меню и название функции, которую необходимо запустить
    :param title: название меню
    :param main: True - главное меню
    """

    while True:
        max_len_title = max(len(f"{i}. {item['name']}") for i, item in enumerate(menu, 1))
        if max_len_title > len(title):
            line = title.center(max_len_title, "-")
        else:
            line = title
        msg_error_num = ''
        print_color(f"{line}", "yellow", True, False)
        try:
            for i in range(len(menu)):
                r = i + 1
                # msg = f"[{r}]. {menu[i]["name"]}"
                # print_color(msg, "Blue", False, False)
                msg = f"{COLOR_ITEM_MENU}{r}{COLOR_RESET}. {menu[i]["name"]}"
                print(msg)
            print("-" * max_len_title)
            if main:
                # msg = f"[{KEY_RETURN[0]}] / [{KEY_EXIT[0]}] - {KEY_EXIT[1]}"
                msg = (f"{COLOR_ITEM_MENU}{KEY_RETURN[0]}{COLOR_RESET} / "
                      f"{COLOR_ITEM_MENU}{KEY_EXIT[0]}{COLOR_RESET} - {KEY_EXIT[1]}")
                print(msg, "\n")
            else:
                msg = f"{TXT_RETURN} ([{KEY_EXIT[0]}] - {KEY_EXIT[1]})"
                # msg = f"{TXT_RETURN} ({COLOR_ITEM_MENU}{KEY_EXIT[0]}{COLOR_RESET} - {KEY_EXIT[1]})"
                print_color(msg, "Blue", False)

            choice = input("Выберите: ")

            check_for_exit(choice, main)

            if choice == KEY_RETURN[0]:
                return None

            msg_error_num = f"Укажите правильно номер пункта. Доступные значения от 0 до {len(menu) + 1}"
            if not choice or choice.isspace():
                raise ValueError(msg_error_num)

            if choice.isdigit():
                choice = int(choice)
                if 0 < choice <= len(menu) + 1:
                    func_run = menu[choice - 1]["menu_func"]
                    func = globals().get(func_run)  # находим функция
                    if callable(func):  # проверяю исполнимая она?
                        func()  # вызов
                    else:
                        raise ValueError(f"Функция '{func_run!r}' не найдена")
                else:
                    raise ValueError(msg_error_num)
            else:
                raise ValueError(f"Неверный формат ввода: '{choice}'")

        except ValueError as e:
            print_error(f"{e}")
        except IndexError:
            print_error(msg_error_num)
        except TypeError as e:
            print_error(f"{e}")


def main_menu():
    """ Точка входа в программу """

    form_menu(MAIN_MENU, " [Главное меню] ", True)


def menu_statistics():
    """ Меню статистики """

    form_menu(MENU_STATISTICS, " [Статистика запросов] ")


def search_by_title():
    """ Команда поиска по ключевому слову в названии фильма """

    while True:
        msg = f"Введите ключевое слово для поиска в названии ([Enter] - {KEY_RETURN[1]} / {TXT_EXIT}) 🔑"
        keyword = input_color(msg, "Cyan").strip().upper()

        check_for_exit(keyword)

        if not keyword or keyword.isspace():
            return None

        # находим общее количество совпавших фильмов
        # хотя по умолчанию MySQL не учитывает регистр и в БД "sakila" названия фильмов записаны полностью в верхнем регистре,
        # на всякий случай приведём к одному регистру, завтра могут появиться другие данные или изменятся настройки ядра БД
        select_parm = (f"%{keyword}%",)
        msg_search = f"Поиск по ключевому слову {COL_KEYWORD_MONGO[2]}'{keyword}'"
        row_cnt = display_page_by_page(select_by_title_cols, select_by_title_body, select_parm, msg_search, keyword)
        if row_cnt:  # записываем в историю поиска
            param = {"keyword": keyword}
            db_connector.insert_log(SEARCH_TYPE[0], param, row_cnt)

            return


def search_by_category():
    """ Команда поиска по жанру и годам (мин-макс) выпуска фильма """

    categories = db_connector.query_execute(select_all_category, fetch="all")
    # вывод результата в таблицу
    print_color("[Список найденных жанров]", "yellow", True, False)
    # добавляем колонки в таблицу кроме последней (category_id нужна для быстрого поиска, что бы не делать 3-й JOIN)
    cols = ["№"]
    cols.extend(list(categories[0])[:-1])
    # добавляю строки в таблицу (кроме category_id)
    rows = [[i] + [item[col] for col in cols[1:]] for i, item in enumerate(categories, 1)]

    display_page(cols, rows, 1, 1, False)
    string = ''
    while True:
        try:
            msg = f"Введите Номер / Название жанра из списка ({TXT_RETURN} / {TXT_EXIT})"
            string = input_color(msg, "Cyan")

            check_for_exit(string)
            if not string:
                print_error(f"Не указан Номер / Название жанра!")
                continue
            if string == KEY_RETURN[0]:
                return None

            category_selected = {}
            if string.isdigit():
                num = int(string)
                if 1 <= num <= len(categories):
                    enumerate(categories, 1)
                    category_selected = categories[num - 1]
                else:
                    print_error(f"Жанр под номером {string} в списке не найдена.")
            else:
                category_selected = list(filter(lambda d: d[COL_CATEGORY].upper() == string.upper(), categories))[0]

            if category_selected:
                search_parm = defaultdict()
                search_parm[COL_CATEGORY_ID] = category_selected[COL_CATEGORY_ID]
                search_parm[COL_CATEGORY] = category_selected[COL_CATEGORY]
                year_min, year_max = category_selected[COL_YEAR_MIN], category_selected[COL_YEAR_MAX]
                display_selected_category(search_parm)
                while True:
                    year_start = input_year(COL_YEAR_MIN, year_min, year_max)
                    if year_start is None:

                        return None

                    elif year_start == -1:
                        continue
                    elif year_start:
                        search_parm["year_start"] = year_start
                        display_selected_category(search_parm)
                        while True:
                            year_stop = input_year(COL_YEAR_MAX, year_start, year_max)
                            if year_stop is None:

                                return None

                            elif year_stop == -1:
                                continue
                            elif year_stop:
                                search_parm["year_stop"] = year_stop
                                row_cnt = display_by_category(search_parm, False)
                                if row_cnt:  # записываем в историю поиска
                                    param = {
                                        "genre_name": search_parm[COL_CATEGORY],
                                        "year_start": search_parm["year_start"],
                                        "year_stop": search_parm["year_stop"]
                                    }
                                    db_connector.insert_log(SEARCH_TYPE[1], param, row_cnt)
                                return
                            else:
                                continue
                    else:
                        continue

        except IndexError:
            print_error(f"Жанр '{string}' в списке не найдена.")

        except Exception as e:
            print_error(f"Что то пошло не так:\n{e}")


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
    title = next(item["name"] for item in MENU_STATISTICS if item["menu_func"] == menu_item_func)
    # удаляем первое слово BEGIN_MSG_STATISTICS ("Посмотреть")
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


if __name__ == "__main__":
    main_menu()
