from datetime import datetime
from project.homelib import *
from project.homelib_db import *


bd_worker = StalCraft()

item_id = "nj29"
path = "stalcraft/project/files/listing.json"
region_mask = 'RU'

# print(bd_worker.seach_lot_active(item_id, region_mask, get_param))

# вставляем данные по истории лотов по ID предмета
# db_history_insert(bd_worker.seach_lot_history(item_id, region_mask, get_param))

# заполняем список всех предметов
# db_item_lst_insert(get_list_items_for_bd(loadjson(path)))

# выводим словарь ID предметов с последней датой загрузки
# print(db_item_list_with_lts_dt())

# выводим список всех ID предметов
# print(db_item_list())

# выводим дату последней вставки по ID предмета
# print(db_item_last_dt(item_id))


item_cnt = len(db_item_list_with_lts_dt())
for item_pos,(key,values) in enumerate(db_item_list_with_lts_dt().items()):
      print(f'{datetime.datetime.now()} Всего ID: {item_cnt} осталось загрузить {item_cnt - item_pos}, загружено {item_pos}')
      result = bd_worker.seach_lot_history(key, region_mask, datelike= values)
      db_history_insert(result)
