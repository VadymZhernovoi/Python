from main import (show_popular_category, show_popular_keyword, get_last_keyword, get_last_category, get_last_uniq)
from modules.io_manager import show_statistics

def show_single():

    tabl = show_popular_category()
    #tabl = ['w']
    show_statistics(tabl)

    tabl = get_last_uniq()
    show_statistics(tabl)

    return None


def show_full():

    tabl_keyword = show_popular_keyword()
    tabl_category = show_popular_category()
    #tabl_keyword = []
    show_statistics(tabl_keyword, tabl_category)

    tabl_keyword = get_last_keyword()
    tabl_category = get_last_category()
    # tabl_keyword = []
    show_statistics(tabl_keyword, tabl_category)

    return None


show_single()

show_full()
