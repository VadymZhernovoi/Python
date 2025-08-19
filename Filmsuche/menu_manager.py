from modules.parm_const import MENU, COLOR_RESET, COLOR_ITEM_MENU, KEY_EXIT, TXT_RETURN
from modules.io_manager import print_color, check_for_exit

def search_by_title(): print("🔍  Поиск по названию...")


def search_by_category(): print("🔍  Поиск по жанру и годам...")


def show_popular_query(): print("📊  Топ популярных запросов")


def show_last_query(): print("📊  Топ последних запросов")


def show_popular_query_full(): print("📊  Сводная популярность")


def show_last_query_full(): print("📊  Сводная последняя")


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

    def __init__(self, menu_cfg, title="Главное меню"):
        self.title = title
        self.menu_cfg = menu_cfg  # текущий уровень меню
        if self.title == "Главное меню":
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
            # msg = (f"{COLOR_ITEM_MENU}{KEY_RETURN[0]}{COLOR_RESET} / "
            #       f"{COLOR_ITEM_MENU}{KEY_EXIT[0]}{COLOR_RESET} - {KEY_EXIT[1]}")
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
            num = input("Выберите пункт --> ").strip()
            check_for_exit(num,  self.main)
            if num.isdigit():
                num = int(num)
                if 0 <= num <= len(self.menu_cfg):
                    return num
            msg_error_num = f"⛔ Укажите правильно номер пункта. Доступные значения от 0 до {len(self.menu_cfg)}!"
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
            print(f"⚠️ Функция '{func_name}' не найдена.")


if __name__ == "__main__":
    MenuManager(MENU, "Главное меню").run()
    print("До свидания 👋")