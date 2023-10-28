import sys
import config.global_var as gv

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from service.index import TransactionInfoPlatform
from utils.SqliteOperator import SqliteOperator
from config.init_db import *


def init_db_struct(db: SqliteOperator):
    """
    初始化表结构
    :param db:
    :return:
    """
    db.execute(create_table_announcement_info)
    db.execute(create_table_announcement_detail)


if __name__ == '__main__':
    # 连接数据库并初始化
    dbConnect = SqliteOperator('./storage/transactionInfo')
    init_db_struct(dbConnect)
    # 初始化全局变量对象
    gv._init()
    app = QApplication(sys.argv)
    ex = TransactionInfoPlatform(dbConnect)
    app.setWindowIcon(QIcon("./imgs/菠萝.svg"))
    ex.show()
    sys.exit(app.exec_())




