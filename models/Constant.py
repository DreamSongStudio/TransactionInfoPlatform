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


class StopType(Enum):
    """
    停止类型
    """
    URL = 1
    DATE = 2

