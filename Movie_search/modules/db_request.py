from .parm_const import COL_CATEGORY, COL_YEAR_MAX, COL_YEAR_MIN, COL_FILM_CNT, COL_FILM, COL_FILM_YEAR

# запрос для выборки списка категорий

select_all_category = f"""
    SELECT
        c.name              AS "{COL_CATEGORY}",
        MIN(f.release_year) AS "{COL_YEAR_MIN}",
        MAX(f.release_year) AS "{COL_YEAR_MAX}",
        COUNT(*)            AS "{COL_FILM_CNT}",
        c.category_id
    FROM category      AS c
    JOIN film_category AS fc ON fc.category_id = c.category_id
    JOIN film          AS f  ON f.film_id      = fc.film_id
    GROUP BY c.category_id, c.name               
    ORDER BY c.name;
    """

# ------------------------------------------------------------
# шапка и тело запроса для поиска по названию фильма
select_by_title_cols = f"""
    title AS '{COL_FILM}', 
    release_year AS '{COL_FILM_YEAR}'
    """
select_by_title_body = """
    FROM 
        film
    WHERE 
        UPPER(title) LIKE %s
    ORDER BY 
        title
    """
# порядок параметров для запроса !!!
# select_parm = (f"%{keyword.upper()}%",)

# ------------------------------------------------------------
# шапка и тело запроса для поиска по категории и годам
select_by_category_cols = f"""
    f.title AS '{COL_FILM}', 
    f.release_year AS '{COL_FILM_YEAR}'
    """
select_by_category_body = """
    FROM film_category AS fc        
    JOIN film AS f
    ON f.film_id = fc.film_id
    WHERE fc.category_id = %s
        AND f.release_year BETWEEN %s AND %s
    ORDER BY f.title
    """
# порядок параметров для запроса !!!
# select_parm = (search_parm[COL_CATEGORY_ID], search_parm["year_start"], search_parm["year_stop"])