import psycopg2

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
          cursor.execute('select * from stalcraft.auctioneer.item_list t')
          print(cursor.fetchall())

    # выводим ошибку при ее возникновлении
except Exception as _ex:
     print("[INFO] Error while working with PostgreSQL", _ex)

    # закрываем соединение и выводим уведомление
finally:
     if connection:
          connection.close()
          print("[INFO] PostgreSQL connection closed")

# Криток лошок, но не конь