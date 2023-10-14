

from get_announcement_index import get_announcement_index
from utils.Common import HOUSE_BUILDING, MUNICIPAL_ENGINEERING, DataModule
from utils.SqliteOperator import SqliteOperator
from utils.FormatDate import parse_date
from config.init_db import *

# 获取房屋建筑数据
# get_announcement_index(MUNICIPAL_ENGINEERING)

# 详情
# du1 = 'http://www.gzggzy.cn/jyywjsgcfwjzzbgg/959057.jhtml'
# get_announcement_detail(du1)


def init_db_struct(db: SqliteOperator):
    """
    初始化表结构
    :param db:
    :return:
    """
    db.execute(create_table_announcement_info)
    db.execute(create_table_announcement_detail)


def spider_data(db: SqliteOperator, module: dict):
    """
    获取数据，并保存入库
    :param db:  SqliteOperator
    :param module: Common
    :return: 新数据条数
    """
    # 获取中止位数据，即该模块下的最新一条info数据的url
    stop_data = db.query(f'select * from announcement_info '
                         f'where module={module["code"]} order by id desc limit 1', 'one')
    print('中止位数据：', stop_data)
    detailIndex, detailMap = get_announcement_index(module, stop_data['url'] if stop_data else '')
    if not detailIndex:
        print('此次扫描未发现新数据！')
        return 0
    # 数据入库
    # 存announcement_info
    save_info_data = [tuple(i.values()) for i in detailIndex]
    keys_count = detailIndex[0].keys().__len__()
    # 插入时反转下数据列表，保证最后一条入库的数据，就是页面上最新的数据
    db.executemany(f"insert into announcement_info {tuple(detailIndex[0].keys())}"
                   f"values ({','.join(['?' for i in range(keys_count)])})",
                   save_info_data[::-1])

    # 然后以announcement_info中的url为条件，查询刚刚插入的数据，以获取id来给announcement_detail进行绑定
    query_info_url_param = [i['url'] for i in detailIndex]
    query_info_url_param.append('-9')
    announcement_info_data_list = db.query(f'select * from announcement_info '
                                           f'where url in {tuple(query_info_url_param)}')

    # 转为{url:id}的形式以方便获取数据
    announcement_info_data_map = {i['url']: i['id'] for i in announcement_info_data_list}

    # 保存announcement_detail
    save_detail_data = []
    save_detail_column = []
    # 补充infoId
    for _k, _v in detailMap.items():
        _v['info_id'] = announcement_info_data_map[_k]
        save_detail_data.append(tuple(_v.values()))
        # insert的列名
        save_detail_column = _v.keys()
    keys_count = save_detail_data[0].__len__()
    db.executemany(f"insert into announcement_detail {tuple(save_detail_column)}"
                   f"values ({','.join(['?' for i in range(keys_count)])})",
                   save_detail_data)

    return len(detailIndex)


if __name__ == '__main__':
    # 连接数据库并初始化
    dbConnect = SqliteOperator('transactionInfo')
    init_db_struct(dbConnect)
    spider_data(dbConnect, DataModule.HOUSE_BUILDING.value)



