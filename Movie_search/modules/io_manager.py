from sys import exit
from prettytable import PrettyTable
from rich.console import Console
from rich.prompt import Prompt
import re

from .db_connector import db_connector
from .constants import (PAGE_SIZE, COL_YEAR_MAX, MONGO_COLS, TOP_QUERIES, COL_SEPARATOR,
                              COL_KEYWORD_MONGO, KEY_RETURN, TXT_RETURN, KEY_EXIT, TXT_EXIT,
                              SEARCH_TYPE, COL_CATEGORY, COL_CATEGORY_MONGO, COL_YEAR_START_MONGO,
                              COL_YEAR_STOP_MONGO, COL_CNT_KEYWORD, COL_CNT_CATEGORY)

console = Console(force_terminal=True, color_system="truecolor")
_BRACKETS = re.compile(r"\[([^]]+)]")  # компилируем регулярное выражение в объект шаблона для repl_brackets()


def repl_brackets(msg: str, color: str = "red"):
    """
    Функция замены в строке "самодельных" управляющих символов на символы форматирования для модуля rich
    Выделяемы символы должны быть взяты в [], например: "Укажите [#] - номер страницы"
    Заменяет "[" -> "[color]" и "]" -> "[/color]"
    :param msg: строка, которую надо отформатировать
    :param color: цвет ("red", "blue"...)
    :return: отформатированная строка
    """
    return _BRACKETS.sub(rf"[{color.lower()}]\1[/{color.lower()}]", msg)


def input_color(msg: str, color: str = "red", before: bool = True) -> str:
    """
    Ввод через консоль строки (сообщение выдаётся в цвете) через Prompt.ask
    Выделяемы символы должны быть взяты в [], например: "Укажите [#] - номер страницы"
    :param msg: сообщение для вывода
    :param color: цвет ("red", "blue"...)
    :param before: True - пропустить одну строку перед вводом
    :return: введенная строка
    """
    msg_color = repl_brackets(msg, color.lower())  # отформатируем строку
    if before:
        print()

    return str(Prompt.ask(msg_color, console=console)).strip()


def print_color(msg: str, color: str = "red", before: bool = True, after: bool = True):
    """
    вывод через консоль строки (сообщение выдаётся в цвете) через console.print
    Выделяемы символы должны быть взяты в [], например: "Навигация: [#] - номер страницы"
    :param msg: стока вывода
    :param color: цвет
    :param before: True - пропустить одну строку перед выводом
    :param after: True - пропустить одну строку после вывода
    :return:
    """
    msg_color = repl_brackets(msg, color.lower())  # отформатируем строку
    if before:
        print()
    console.print(msg_color)
    if after:
        print()

    return None


def check_for_exit(string: str, main_menu: bool = False):
    """
    Проверка на введенное пользователем значение. Если значение равно символу "выйти из программы",
    то программа ещё раз переспрашивает (если это не главное меню) и при утвердительном ответе выдаёт
    сообщение о завершении и закрывает программу через exit(0)
    :param string: введенное пользователем значение
    :param main_menu: True - главное меню
    :return: bye, bye
    """
    if main_menu and string in (KEY_EXIT[0], KEY_RETURN[0]):
        print_color("Спасибо за внимание! До встречи.", "cyan")

        exit(0)  # закрыть программу

    if string == KEY_EXIT[0]:
        msg = "Вы действительно хотите выйти из программы ([y]/[Y] - выйти, [любое] - остаться)"
        key = input_color(msg, "red")
        if key.lower() == 'y':
            print_color("Спасибо за внимание! До встречи.", "cyan")

            exit(0)  # закрыть программу


def print_error(msg: str, before: bool = False):
    """
    печатает в консоль сообщение об ошибке
    фраза "Ошибка!" выводится красным цветом, а само сообщение желтым цветом
    :param msg: само сообщение
    :param before: True - пропускает строку перед выводом сообщения
    :return:
    """
    # console = Console(force_terminal=True, color_system="truecolor")
    if before:
        print()
    console.print(f"[red]Ошибка![/red] [yellow]{msg}[/yellow]")

    return None

def is_list_of_dicts_not_empty(data):
    """
    Проверяет, не пустой ли список словарей
    :param data: Список, содержащий словари.
    :return: True, если список не пуст, иначе - False.
    """
    if not data:
        return False

    for dictionary in data:

        if dictionary:

            if type(dictionary) is not dict:
                return False

            if dictionary == {}:
                return False

            return True

    return False


def display_page(cols: list, rows: list[list], page_num: int, total_pages: int, footer: bool = True, *alignment):
    """
    выводит в консоли страницу в виде таблицы
    :param cols: список из названий столбцов
    :param rows: строки таблицы
    :param page_num: номер текущей страницы
    :param total_pages: всего страниц
    :param footer: True - напечатать пустую строку после вывода страницы
    :param alignment: кортеж из названия столбца и способ выравнивания текста (("col_names", "r") - выравнивание справа)
    :return:
    """
    # Создание объекта таблицы
    table = PrettyTable()
    table.field_names = cols  # шапка таблицы
    table.align[COL_SEPARATOR] = "l"
    table.align[MONGO_COLS["search_type"]] = "l"
    table.align[MONGO_COLS[COL_CATEGORY_MONGO[0]]] = "l"

    for align in alignment:
        table.align[align[0]] = align[1]

    # вывод страницы
    for row in rows:
        table.add_row(row)  # Добавление строк в таблицу

    print(table)
    if footer:
        print(f"--- Страница {page_num} из {total_pages} ---")

    return None


def input_year(txt: str, year_min: int, year_max: int) -> int | None:
    """
    функция ввода года
    :param txt: значение, введенное пользователем
    :param year_min: минимальное доступный год
    :param year_max: максимально доступный год
    :return: год, если условия ввода выполнены, или None - если не выполнены
    """
    year_enter = year_max if txt == COL_YEAR_MAX else year_min
    print_color(f"Укажите [{txt}].", "yellow", True, False)
    msg = f"Доступные значения: [{year_min}] - [{year_max}] ([Enter] - {year_enter}, {TXT_RETURN}, {TXT_EXIT}) -->"
    string = input_color(msg, "Cyan", False)
    try:
        check_for_exit(string)

        if string == KEY_RETURN[0]:
            return None

        if not string or string.isspace():
            return year_enter

        if string.isdigit():
            year = int(string)
            if year_min <= year <= year_max:

                return year

            else:
                raise ValueError(f"Доступные значения: {year_min} - {year_max}")
        else:
            raise ValueError(f"Неверный формат ввода '{string}'")

    except ValueError as e:
        print_error(f"{e}", True)

        return - 1

    except Exception as e:
        print_error(f"Что то пошло не так:\n{e}", True)

        return -1


def check_rows_cnt(rows: list) -> list:
    """
    проверяет кол-во строк, если меньше TOP_QUERIES - добавляет пустыми значениями до TOP_QUERIES
    :param rows: строки
    :return:
    """
    length = len(rows)
    # если мало запросов, то строк буде меньше чем TOP_QUERIES
    if length < TOP_QUERIES:
        cnt_cols = len(rows[0]) if rows else 0  # сколько колонок добавить
        add_rows = max(0, TOP_QUERIES - length)  # сколько строк добавить
        rows.extend([[' '] * cnt_cols for _ in range(add_rows)])  # добавляем строки с пустыми значениями

    return rows


def create_row(item: dict, add_empty_col: bool = False) -> list:
    """
    создаёт строку на основе словаря item
    :param item: сам словарь
    :param add_empty_col: True - добавляет две пустые колонки, что бы количество колонок было сопоставимо с длинным словарём
    :return: строку
    """
    row = []
    for key, value in item.items():
        if value in SEARCH_TYPE:  # только для search_type
            row.append(f"{COL_KEYWORD_MONGO[1]}" if value == SEARCH_TYPE[0] else f"{COL_CATEGORY}")
            continue
        if key == COL_KEYWORD_MONGO[0]:  # label or key in SEARCH_TYPE[0]:  # только для keyword или category
            row.append(f"{COL_KEYWORD_MONGO[2]}'{value}'")
            if add_empty_col:
                row.extend([''] * 2)
        else:
            row.append(str(f"{value}"))

    return row


def show_statistics(tabl_first: list[dict], tabl_second: list[dict] = ''):
    """
    Показывает статистику по запросам. Определяет кол-во таблиц в выводе запроса - если одна, то выводит одинарную
    таблицу, если две - выводит двойную таблицу
    :param tabl_first:
    :param tabl_second:
    :return:
    """
    is_tabl_first = is_list_of_dicts_not_empty(tabl_first)
    is_tabl_second = is_list_of_dicts_not_empty(tabl_second)
    if not (is_tabl_first or is_tabl_second):
        print_color("[Данных не найдено!]", "yellow")

        return None

    if not (is_tabl_first and is_tabl_second):
        show_single_statistics(tabl_first)
    else:
        show_double_statistics(tabl_first, tabl_second)


def add_cols_and_row_in_table(tabl: list, cols: list, row: list):
    """ Добавляет колонки по ключам и сформированную строку """
    for key in tabl[0].keys():
        cols.append(key)
    row = add_row_in_table(tabl, row)

    return cols, row


def add_row_in_table(tabl, row: list, add_empty_col: bool = False):
    for _, item in enumerate(tabl, start=1):
        row_part = create_row(item, add_empty_col)
        row.append(row_part)

    return row


def add_rows_in_table_out(row, rows):
    for i in range(len(row)):
        row_cur = [i + 1] + row[i]  # добавляю номер строки
        rows.append(row_cur)

    return rows


def show_single_statistics(tabl: list[dict]):
    """
    выводит одинарную таблицу по статистике запросов
    :param tabl: список со вложенными словарями - данные для таблицы
    :return:
    """
    if not is_list_of_dicts_not_empty(tabl):
        print_color("[Данных не найдено!]", "yellow")

        return None

    cols, rows = [], []
    max_dict = max(tabl, key=len)  # находим словарь с максимальным кол-вом ключей, т.к. словари разной длины
    for key in max_dict.keys():  # добавляем колонки по ключам
        cols.append(key)
    rows = add_row_in_table(tabl, rows, True)
    # print(tabl, rows)
    # for i, item in enumerate(tabl, start=1):
    #     row = create_row(item, True)
    #     rows.append(row)
    for i in range(len(rows)):
        rows[i] = [i + 1] + rows[i]
    cols = ["№"] + cols
    cols_ru = [MONGO_COLS.get(col, col) for col in cols]  # приведу названия столбцов в удобочитаемый вид
    align = ((MONGO_COLS[COL_CATEGORY_MONGO[0]], "l"), (MONGO_COLS["search_type"], "l"))

    display_page(cols_ru, rows, 1, 1, False,align)

    return None


def combined_lists(tabl_first: list[dict], tabl_second: list[dict]):
    if is_list_of_dicts_not_empty(tabl_first) and is_list_of_dicts_not_empty(tabl_second):
        combined = sorted(tabl_first + tabl_second,  # склеиваем два результата выборки
                          key=lambda d: d.get(COL_CNT_KEYWORD, d.get(COL_CNT_CATEGORY, 0)),
                          # сортируем по ключам COL_CNT_KEYWORD и COL_CNT_CATEGORY
                          reverse=True)[:TOP_QUERIES]  # сортируем в обратном порядке и оставляем только TOP_QUERIES

        return combined

    else:
        print_color("[Данных не найдено!]", "yellow")

        return None


def show_double_statistics(tabl_first: list[dict], tabl_second: list[dict]):
    """
    выводит двойную таблицу по статистике запросов
    :param tabl_first: список со вложенными словарями первой таблицы - данные для первой таблицы
    :param tabl_second: список со вложенными словарями вторй таблицы - данные для вторй таблицы
    :return:
    """
    is_tabl_first = is_list_of_dicts_not_empty(tabl_first)
    is_tabl_second = is_list_of_dicts_not_empty(tabl_second)
    if not (is_tabl_first or is_tabl_second):
        print_color("[Данных не найдено!]", "yellow")

        return None

    row_first, row_second, rows, cols = [], [], [], []
    if is_tabl_first:
        cols, row_first = add_cols_and_row_in_table(tabl_first, cols, row_first)
        row_first = check_rows_cnt(row_first)  # проверяем кол-во строк в tabl_first, вдруг меньше TOP_QUERIES
    if is_tabl_second:
        if len(cols) > 1:
            cols += ["and"]
        cols, row_second = add_cols_and_row_in_table(tabl_second, cols, row_second)
        row_second = check_rows_cnt(row_second)  # проверяем кол-во строк в tabl_second, вдруг меньше TOP_QUERIES
    rows = []
    if is_tabl_first and is_tabl_second:
        for i in range(TOP_QUERIES):
            # соединяю строки из двух таблиц в одну строку и добавляю номер строки
            row = [i + 1] + row_first[i] + ['✯' * (TOP_QUERIES - i)] + row_second[i]
            rows.append(row)
    elif is_tabl_first:
        rows = add_rows_in_table_out(rows, row_first)
    else:
        for i in range(len(row_second)):
            rows = add_rows_in_table_out(rows, row_second)

    cols = ["№"] + cols
    cols_ru = [MONGO_COLS.get(col, col) for col in cols]  # приведу названия столбцов в удобочитаемый вид

    display_page(cols_ru, rows, 1, 1, False, (COL_KEYWORD_MONGO[1], "l"))


def display_page_by_page(select_col: str, select_body: str, parm_find: tuple, search: str = ''):
    """
    Команда постраничного вывода таблицы.
    Организовано кэширование запросов.
    Есть возможность листать вперёд/назад и указывать номер страницы
    :param select_col: перечень столбцов, которые ад вывести в SQL запросе
    :param select_body: тело самого SQL запроса
    :param parm_find: параметры, передаваемые в условия SQL запрос
    :param search: сообщение по чему ищем
    :return:
    """
    select_col = select_col.strip()
    select_body = select_body.strip()
    request_cnt = f"SELECT COUNT(*) {select_body}"
    result = db_connector.query_execute(request_cnt, params=parm_find, fetch="one")
    total_rows = result['COUNT(*)']
    if total_rows == 0:
        print_color("[Фильмы не найдены.]", "yellow", False, False)

        return None

    total_pages = (total_rows + PAGE_SIZE - 1) // PAGE_SIZE

    query = f"SELECT {select_col} {select_body} LIMIT %s OFFSET %s"
    offset = 0
    # делаем кеш для страниц фильмов
    cache = {}
    outer = True

    while outer:
        if offset not in cache:
            parm = parm_find + (PAGE_SIZE, offset)
            cache[offset] = db_connector.query_execute(query, params=parm, fetch="all")  # кеш для страниц фильмов
        films = cache[offset]
        # вывод текущей страницы
        cols = ["№"]
        cols.extend(films[0].keys())
        rows = list()
        page_num = offset // PAGE_SIZE + 1
        for r, film in enumerate(films[:PAGE_SIZE], start=1):
            row = [r + (page_num - 1) * PAGE_SIZE]
            for i in range(1, len(cols)):
                row.append(film[cols[i]])
            rows.append(row)
        if search:
            print_color(search, "yellow", True, False)
        print_color(f"Найдено фильмов: [{total_rows}]   (Всего страниц: [{total_pages}])", "cyan", True, False)
        display_page(cols, rows, page_num, total_pages, True if total_pages > 1 else False)
        # навигация
        msg = f"{TXT_RETURN} / {TXT_EXIT}"
        if total_pages <= 1:
            break

        msg = "[#] -номер_страницы / " + msg
        if page_num < total_pages:
            msg = "[+] -след. / " + msg
        if page_num > 1:
            msg = "[-] -пред. / " + msg

        while True:
            nav = input_color(f"Навигация: {msg}", "cyan", False).lower()
            print()
            check_for_exit(nav)

            if nav == KEY_RETURN[0]:
                outer = False

                break

            elif nav in ("-", "/"):
                if offset >= PAGE_SIZE:
                    offset -= PAGE_SIZE

                    break

                else:
                    print_color("[⏮] Вы на первой странице.", "red", False, False)

                    continue

            elif not nav or nav in ("+", "ъ"):
                if offset + PAGE_SIZE < total_rows:
                    offset += PAGE_SIZE

                    break

                else:
                    print_color("[⏭] Это последняя страница.", "red", False, False)

                    continue

            elif nav.isdigit():
                page = int(nav)
                if 1 <= page <= total_pages:
                    offset = (page - 1) * PAGE_SIZE

                    break

                else:
                    print_color(f"⛔ Страницы [{page}] не существует (доступны [1]-[{total_pages}])", "red", False,
                                False)

                    continue

            else:
                print("⛔ Неизвестная команда. Используйте только доступные команды!")

                continue

    return total_rows


def display_selected_category(search_parm: dict, print_run: bool = True) -> str:
    """
    формирование строки параметров поиска по категория+года
    :param search_parm: категория, год с, год по
    :param print_run: True - вывести параметры поиска
    :return: строка сообщения с выбранными параметрами поиска категория + года
    """
    msg = "Вы выбрали"
    for key, value in search_parm.items():
        if key == COL_CATEGORY:
            msg += f" {COL_CATEGORY} ['{value}']"
        elif key == f"{COL_YEAR_START_MONGO[0]}":
            msg += f", год с [{value}]"
        elif key == f"{COL_YEAR_STOP_MONGO[0]}":
            msg += f" по [{value}]"
    if print_run:
        print_color(msg, "yellow", True, False)

    return msg
