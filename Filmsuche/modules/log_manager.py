from .db_connector import db_connector
from .parm_const import TOP_QUERIES, COL_CNT_CATEGORY, COL_CNT_KEYWORD, SEARCH_TYPE

def get_last_uniq():
    pipeline = [
        {'$group': {
            '_id': '$params',                           # группируем по группе params - определяем УНИКАЛЬНЫЕ запросы
            'cnt': {'$sum': 1}, 
            'search_type': {'$first': '$search_type'},  # сохраняем для pipeline поле search_type
            'timestamp': {'$last': '$timestamp'}        # сохраняем для pipeline ПОСЛЕДНЮЮ дату УНИКАЛЬНОГО запроса
        }},
        {'$sort': {'timestamp': -1}},
        {'$limit': TOP_QUERIES},
        {'$replaceRoot': {
            'newRoot': {
                '$mergeObjects': [                      # добавляем нужные поля в нужном порядке
                    {'timestamp': '$timestamp',
                    'search_type': '$search_type'},
                    '$_id',                              # расплющиваем объект params
                    {'results_count': '$results_count',
                    'cnt': '$cnt'}
                ]
            }
        }},
    ]

    return db_connector.read_log(pipeline)

def get_last_keyword():
    pipeline = [
        {'$match': {'search_type': SEARCH_TYPE[0]}},
        {'$group': {
            '_id': '$params.keyword',
            'cnt': {'$sum': 1},
            'search_type': {'$first': '$search_type'},  # сохраняем для pipeline поле search_type
            'timestamp': {'$last': '$timestamp'}        # сохраняем для pipeline ПОСЛЕДНЮЮ дату УНИКАЛЬНОГО запроса
        }},
        {'$sort': {'timestamp': -1}},
        {'$limit': TOP_QUERIES},
        {'$replaceRoot': {
            'newRoot': {
                '$mergeObjects': [  # добавляем нужные поля в нужном порядке
                    {
                        'timestamp': '$timestamp',
                        #'search_type': '$search_type',
                        'keyword': '$_id',
                        COL_CNT_KEYWORD: '$results_count',
                        'cnt': '$cnt'
                    }
                ]
            }}
        }
    ]

    return db_connector.read_log(pipeline)

def get_last_category():
    pipeline = [
        {'$match': {'search_type': SEARCH_TYPE[1]}},
        {'$group': {
            '_id': '$params',
            'cnt': {'$sum': 1 },
            'search_type': {'$first': '$search_type'},
            'timestamp': {'$last': '$timestamp'}
        }},
        {'$sort': {'timestamp': -1}},
        {'$limit': TOP_QUERIES},
        {'$replaceRoot': {
            'newRoot': {
                '$mergeObjects': [  # добавляем нужные поля в нужном порядке
                    {
                        'date': '$timestamp',},
                        #'search_type': '$search_type'},
                        '$_id',          # расплющиваем объект params
                        {'results': '$results_count',
                        COL_CNT_CATEGORY: '$cnt'
                    }
                ]
            }}
        }
    ]

    return db_connector.read_log(pipeline)


def show_popular_keyword():
    pipeline = [
        {"$match": {"search_type": "keyword"}},
        {"$group": {
            "_id": {"$toUpper": "$params.keyword"},
            "cnt": {"$sum": 1},
            "original": {"$first": "$params.keyword"}  # сохраним оригинальный регистр "keyword"
        }},
        {"$replaceRoot": {
            "newRoot": {
                "$mergeObjects": [
                    {"keyword": "$original"},  # покажем оригинальный регистр "keyword"
                    {COL_CNT_KEYWORD: "$cnt"}
                ]
            }
        }},
        {"$sort": {
            COL_CNT_KEYWORD: -1,
            'keyword': 1
        }},
        {"$limit": TOP_QUERIES},
    ]

    return db_connector.read_log(pipeline)


def show_popular_category():
    pipeline = [
        {'$match': {'search_type': 'category_year'}},
        {'$group': {
            '_id': '$params',
            'cnt': {'$sum': 1},
        }},
        {'$replaceRoot': {
            'newRoot': {
                '$mergeObjects': [                  # выводим поля в нужном порядке
                    {'search_type': '$search_type'},
                    '$_id',                         # расплющиваем объект _id (params)
                    {COL_CNT_CATEGORY: '$cnt'}
                ]
            }
        }},
        {'$sort': {
            COL_CNT_CATEGORY: -1,
            'genre_name': 1,
            'year_start': 1,
            'year_stop': 1
        }},
        {'$limit': TOP_QUERIES},
    ]

    return db_connector.read_log(pipeline)


def get_popular():
    pipeline = [
        {'$group': {
            '_id': '$params',
            'cnt': {'$sum': 1},
            "search_type": {"$first": "$search_type"} # сохраняем поле $search_type
        }},
        {'$sort': {
            'cnt': -1,
            "_id": 1
        }},
        {'$limit': TOP_QUERIES},
        {"$replaceRoot": {
            "newRoot": {
                "$mergeObjects": [                     # добавляем нужные поля в нужном порядке
                    {"search_type": "$search_type"},
                    "$_id",                             # расплющиваем объект _id ($params)
                    {COL_CNT_KEYWORD: "$cnt"}
                ]
            }
        }}
    ]

    return db_connector.read_log(pipeline)

# def show_last():
#     pipeline = [
#         {'$replaceRoot': {
#             'newRoot': {
#                 '$mergeObjects': [  # добавляем нужные поля в нужном порядке
#                     {'timestamp': '$timestamp',
#                      'search_type': '$search_type'},
#                     '$params',  # расплющиваем объект params
#                     {COL_CNT_KEYWORD: '$results_count'}
#                 ]
#             }
#         }},
#         {'$sort': {'timestamp': -1}},
#         {'$limit': TOP_QUERIES}
#     ]
#
#     return db_connector.read_log(pipeline)
#
# def show_last_keyword():
#     pipeline = [
#         {'$match': {'search_type': 'keyword'}},
#         {'$sort': {'timestamp': -1}},
#         {'$limit': TOP_QUERIES},
#         {'$replaceRoot': {
#             'newRoot': {
#                 '$mergeObjects': [  # выводим нужные поля в нужном порядке
#                     {'timestamp': '$timestamp'},
#                     '$params',  # расплющиваем объект params
#                     {'results_count': '$results_count'}
#                 ]
#             }
#         }}
#     ]
#
#     return db_connector.read_log(pipeline)
#
# def show_last_category():
#     pipeline = [
#         {'$match': {'search_type': 'category_year'}},
#         {'$sort': {'timestamp': -1}},
#         {'$limit': TOP_QUERIES},
#         {'$replaceRoot': {
#             'newRoot': {
#                 '$mergeObjects': [  # выводим нужные поля в нужном порядке
#                     {'date': '$timestamp'},
#                     '$params',  # расплющиваем объект params
#                     {'result': '$results_count'}
#                 ]
#             }
#         }}
#     ]
#
#     return db_connector.read_log(pipeline)