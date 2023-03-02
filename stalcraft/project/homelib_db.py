import psycopg2

"""
РАБОТА С API
"""
# функция вставки данных из api по истории
def db_history_insert (arrow_db):
    sql_params = 'insert into stalcraft.auctioneer.item_price_hist (item_id,amount,price,sell_time) VALUES'
    sql_type = 'db_insert'
    db_arrow_to_str(arrow_db, sql_params, sql_type)

# функция вставки данных из справочника предметов
def db_item_lst_insert (arrow_db):
    sql_params = 'insert into stalcraft.auctioneer.item_list (item_class,item_type,item_id,item_name_ru,item_name_eu) VALUES'
    sql_type = 'db_insert'
    db_arrow_to_str(arrow_db, sql_params, sql_type)

# функция преобразования полученных данных из API в SQL для втавки   
def db_arrow_to_str (arrow_db, sql_params,sql_type):
    for value in arrow_db:
        sql_type = sql_type
        sql_params += str(value) + ',' 
    db__action((sql_params[:-1]),sql_type)

"""
РАБОТА С ЗАПРОСАМИ В БД
"""
# поиск последней даты по id предмета
def db_item_last_dt (item_id):
    sql_params = f"select max(t.sell_time) as time_limit from stalcraft.auctioneer.item_price_hist t where t.item_id = '{item_id}'"
    sql_type = 'sql_fetch_list'
    return db__action(sql_params, sql_type)

# список всех ID предметов 
def db_item_list():
    sql_params = "select t.item_id as item_id from stalcraft.auctioneer.item_list t"
    sql_type = 'sql_fetch_list'
    return db__action(sql_params, sql_type)

# список всех ID предметов с последней датой вставки
def db_item_list_with_lts_dt():
    sql_params = """select  it.item_id as item_id
		                   ,max(iph.sell_time) as max_sell_time 
                    from stalcraft.auctioneer.item_list it
	                     left join stalcraft.auctioneer.item_price_hist iph on iph.item_id = it.item_id
                    group by it.item_id;"""
    sql_type = 'sql_fetch_dict'
    return db__action(sql_params, sql_type)

"""
ГЛАВНАЯ ФУНКЦИЯ РАБОТЫ С БД
"""

def db__action(sql_values,sql_type):

    from project.db_conf import host, user, password, dbname, port
    # обработка массив для проведения вставки данных в БД
    try:
        # подключаемся к БД
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=dbname,
            port=port
        )
        connection.autocommit = True
        
        with connection.cursor() as cursor:
            cursor.execute(sql_values)
            if sql_type == 'db_insert':
                print("insert all rows done successfully")
            elif sql_type == 'sql_fetch_dict':
                data = cursor.fetchall()
                data_dict = {}
                for i in data:
                    data_dict[i[0]] = i[1]
                return data_dict
            elif sql_type == 'sql_fetch_list':
                data = cursor.fetchall()
                return data
            
    # выводим ошибку при ее возникновлении
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)

    # закрываем соединение и выводим уведомление
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

