from enum import Enum


HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

GLOBAL_URI = 'http://www.gzggzy.cn'

HOUSE_BUILDING = {'jyywjsgcfwjzzbgg'}
MUNICIPAL_ENGINEERING = 'jyywjsgcszgczbgg'


class DataModule(Enum):
    # 房屋建筑
    HOUSE_BUILDING = {'code': 1, 'name': 'jyywjsgcfwjzzbgg'}
    # 市政工程
    MUNICIPAL_ENGINEERING = {'code': 2, 'name': 'jyywjsgcszgczbgg'}


class StopType(Enum):
    URL = 1
    DATE = 2

