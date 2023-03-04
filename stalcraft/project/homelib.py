import requests, json, re, functools, time , datetime
from datetime import datetime as mydate

def timer(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        runtime = time.perf_counter() - start
        print(f"{func.__name__} completed for {runtime:.4f} secs")
        return result
    return _wrapper


def sleep(timeout, retry=3):
    def the_real_decorator(function):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < retry:
                newtimeout = timeout + retries * 5
                try: 
                    value = function(*args, **kwargs)
                except:
                    retries += 1
                    if retries != retry:
                        print(f'Сон на {newtimeout} секунд | Количество оставшихся подключений {retry - retries}')
                        time.sleep(newtimeout) 
                        print('Продолжаю искать...') 
                else:
                    return value
        return wrapper
    return the_real_decorator


class StalCraft:
    post_req = {
                "client_id": "154",
                "client_secret": "YTkkVvfpWiLcImVPTuXUXELmWdt0SOCAyJpG0RWO",
                "grant_type": "client_credentials",
                "scope": ""
                }

    custom_param = {
                'additional' : 'false',
                'limit' : '1',
                'offset' : '0',
                'order' : 'asc',
                'sort' : 'current_price',
                }    

    def __init__(self, post_url = "https://exbo.net/oauth/token", 
                    token = None, access_token = 'Bearer '):
        self.__post_url = post_url #URL по которому получаем токен
        self.__token = token
        self.__access_token = access_token

    @property
    def post_url(self):
        return self.__post_url

    @post_url.setter
    def post_url(self,url):
        if url != "":
            self.__post_url = url
        else:
            raise Exception
    
    @property
    def token(self):
        if self.__token != None:
            return self.__token
        else:
            return self._get_token()

    @property
    def access_token(self):
        if self.__token != None:
            return self.__access_token + self.__token
        else:
            return self.__access_token + self.token

    def _get_token(self):
        if self.post_url != None:
            response = requests.post(self.post_url, json = self.post_req)
            self.__token = response.json()['access_token']
            return self.__token
        else:
            print('Post URL Empty')
    

    @timer
    def seach_lot_active(self, item, region = 'RU', param = None):
        url = f'https://eapi.stalcraft.net/{region}/auction/{item}/lots'
        return self.__seach_lots(url)["lots"]


    @timer
    def seach_lot_history(self, item, region = 'RU', startpos = 0, maxitem = 0, datelike = None):
        def _checkcoutitem(total :int , maxitem : int) -> int:
            return maxitem if  0 != maxitem <= total else total

        def _checklimit(maxitem) -> int:
            return 100 if maxitem > 100 else maxitem

        def _checkdate(element : tuple, date : datetime) -> bool:
            elmdate = mydate.strptime(element, "%Y-%m-%dT%H:%M:%SZ")
            bddate = date if date != None else 0
            return False if elmdate != bddate else True

        def _createlist(itemname : str, buff : tuple, datelike : datetime, title = ('amount','price','time','prices')) -> list:
            list_item = []
            for element in buff[title[3]]:
                if _checkdate(element[title[2]], datelike): break
                list_item.append((itemname , element[title[0]], element[title[1]], element[title[2]]))   
            return list_item

        url = f'https://eapi.stalcraft.net/{region}/auction/{item}/history'
        flag = True
        param_for_seach = {
            'additional' : 'false',
                            }   
        param_for_seach['limit'] = _checklimit(maxitem)
        param_for_seach['offset'] = startpos
        result = []
        while flag:        
            seach_lot_buff = self.__seach_lots(url, param_for_seach)
            print(f"{item} - [{param_for_seach['offset']}/{seach_lot_buff['total']}]")   
            newresult = _createlist(item, seach_lot_buff, datelike)
            maxpos = _checkcoutitem(seach_lot_buff['total'],maxitem) - param_for_seach['limit'] - param_for_seach['offset'] 
            flag = (len(seach_lot_buff['prices']) == len(newresult)) and (maxpos > 0)
            param_for_seach['offset'], param_for_seach['limit'] = param_for_seach['offset'] + param_for_seach['limit'], _checklimit(maxpos)
            result += newresult  
        return result
    
    @sleep(30)
    def __seach_lots(self, url, param = custom_param):
        try:
            get_header = {
                        'Content-Type':'application/json',
                        'Authorization': self.access_token,
                        }
            response = requests.get(url, headers=get_header, params= param).json()
            if response.get('title') != None: raise KeyError
        except:
            print(f'Сервер блок на [{param["offset"]}]')
            raise KeyError
        else:
            
            return response
"""
Конец тела класса
"""

"""
Далее Код для парсинка их штатного JSON в наш "ID - Name"
"""
def loadjson(namefile = "file/title.json") -> json:
    with open(namefile, "r", encoding='utf-8') as read_file:
        return json.load(read_file)

def savejson(jsonarray, namefile = "file/newjson.json"):
    dict = {paritemlist(item['data'])[0][2] if paritemlist(item['data']) != None else ' ':item['name']['lines']['ru'] for item in jsonarray}  # <--- Эту закомментить
    with open(namefile, "w", encoding='utf-8') as write_file:
        json.dump(dict, write_file, indent=4, ensure_ascii=False)
    
def paritemlist(jsonarray, pattern = r'\/\w*\/(\w*)\/?(\w*)\/(\w*).json'):
    ar_text = re.findall(pattern, str(jsonarray)) 
    return ar_text if len(ar_text) != 0 else None

def get_list_items_for_bd(jsonarray) -> dict:
    dict_item = []
    for item in jsonarray:
        dict_item.append((paritemlist(item['data'])[0] if paritemlist(item['data']) != None else ' ')+(item['name']['lines']['ru'], item['name']['lines']['en']) )
    return dict_item



"""
Проверка связи для Максима!
"""