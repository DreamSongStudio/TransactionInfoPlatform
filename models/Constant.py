from enum import Enum


class DataModule(Enum):
    """
    数据所属类别
    """
    # 所有
    ALL = {'code': 0, 'name': '', 'label': '全部'}
    # 房屋建筑
    HOUSE_BUILDING = {'code': 1, 'name': 'jyywjsgcfwjzzbgg', 'label': '房屋建筑'}
    # 市政工程
    MUNICIPAL_ENGINEERING = {'code': 2, 'name': 'jyywjsgcszgczbgg', 'label': '市政工程'}
    # 交通工程
    TRAFFIC_ENGINEERING = {'code': 3, 'name': 'jyywjsgcjtgczbgg', 'label': '交通工程'}
    # 能源电力
    ENERGY_POWER = {'code': 4, 'name': 'jyywjsgcnydlzbgg', 'label': '能源电力'}
    # 市政工程
    RAILWAY_TRACK = {'code': 5, 'name': 'jyywjsgctlgdzbgg', 'label': '铁路轨道'}
    # 水利水务
    WATER_AFFAIRS = {'code': 6, 'name': 'jyywjsgcslswzbgg', 'label': '水利水务'}
    # 林业园林
    FORESTRY_GARDEN = {'code': 7, 'name': 'jyywjsgcyllyzbgg', 'label': '林业园林'}
    # 民航工程
    CIVIL_AVIATION = {'code': 8, 'name': 'jyywjsgcmhgczbgg', 'label': '民航工程'}
    # 部队工程
    ARMY_ENGINEERING = {'code': 9, 'name': 'jyywjsgcbdgczbgg', 'label': '部队工程'}



class StopType(Enum):
    """
    停止类型
    """
    URL = 1
    DATE = 2

