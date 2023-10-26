import math
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime
from component.CustomerLineEdit import CustomWidget
from main import spider_data, init_db_struct
from utils.SqliteOperator import SqliteOperator
from utils.Common import GLOBAL_URI
from models.Constant import DataModule


class window(QWidget):
    def __init__(self, db_connect: SqliteOperator, parent=None):
        super(window, self).__init__(parent)
        self.resize_to_center(200, 100)
        self.monitorPartEdit = None
        self.bidMaxAmountEdit = None
        self.releaseTimeStart = None
        self.releaseTimeEnd = None
        self.moduleSelect = None

        # 设置初始类型为0
        self.module = 0

        # 设置数据库对象
        self.db = db_connect

        self.setWindowTitle("招投标交易信息一览")

        dataViewGrid = QGridLayout()
        self.searchGrid = QGridLayout()
        self.optionsArea = QGridLayout()

        self.init_search_layout()
        self.init_options_area()

        self.tableWidget = QTableWidget()
        dataViewGrid.addWidget(self.tableWidget, 5, 0, 1, 2)

        dataViewGrid.addLayout(self.searchGrid, 0, 0)
        dataViewGrid.addLayout(self.optionsArea, 0, 1)
        self.setLayout(dataViewGrid)

    def init_search_layout(self):
        """
        渲染搜索栏
        :return:
        """
        monitorPartLabel = QLabel("监管部门：")
        self.monitorPartEdit = CustomWidget(self.search_option)

        bidMaxAmountLabel = QLabel("最高限价：")
        self.bidMaxAmountEdit = CustomWidget(self.search_option)

        releaseTimeLabel = QLabel("发布时间：")
        releaseTimeMiddleLabel = QLabel(" 到 ")

        default_date = QDate.currentDate()

        self.releaseTimeStart = QDateEdit()
        self.releaseTimeStart.setCalendarPopup(True)
        self.releaseTimeEnd = QDateEdit()
        self.releaseTimeEnd.setCalendarPopup(True)

        self.releaseTimeStart.setDate(default_date)
        self.releaseTimeEnd.setDate(default_date)

        moduleLabel = QLabel("工程类别：")
        self.moduleSelect = QComboBox()
        for n, v in DataModule.__members__.items():
            self.moduleSelect.addItem(v.value['label'], v.value['code'])
        self.moduleSelect.currentIndexChanged.connect(self.change_data_module)

        self.searchGrid.addWidget(monitorPartLabel, 0, 0)
        self.searchGrid.addWidget(self.monitorPartEdit, 0, 1, 1, 3)

        self.searchGrid.addWidget(bidMaxAmountLabel, 1, 0)
        self.searchGrid.addWidget(self.bidMaxAmountEdit, 1, 1, 1, 3)

        self.searchGrid.addWidget(releaseTimeLabel, 2, 0)
        self.searchGrid.addWidget(self.releaseTimeStart, 2, 1)
        self.searchGrid.addWidget(releaseTimeMiddleLabel, 2, 2)
        self.searchGrid.addWidget(self.releaseTimeEnd, 2, 3)

        self.searchGrid.addWidget(moduleLabel, 3, 0)
        self.searchGrid.addWidget(self.moduleSelect, 3, 1, 1, 3)

    def init_options_area(self):
        """
        渲染操作区域
        :return:
        """
        updateDataButton = QPushButton("更新数据")
        updateDataButton.clicked.connect(self.update_data)

        searchButton = QPushButton("搜索")
        searchButton.clicked.connect(self.search_option)
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        searchButton.setSizePolicy(size_policy)

        self.optionsArea.addWidget(updateDataButton, 0, 0, 1, 1)
        self.optionsArea.addWidget(searchButton, 2, 0, 2, 1)

    def search_option(self):
        """
        搜索数据
        :return:
        """
        monitor_part = self.monitorPartEdit.text()
        bid_max_amount = self.bidMaxAmountEdit.text()
        release_start_time = datetime.strptime(self.releaseTimeStart.text(), '%Y/%m/%d')
        release_end_time = datetime.strptime(self.releaseTimeEnd.text(), '%Y/%m/%d')

        print(f'监管部门：{monitor_part}， '
              f'最高限价：{bid_max_amount}， '
              f'发布时间：{release_start_time.timestamp()}到{release_end_time.timestamp()}')

        sql = (
            f'select ai.project_no 项目编号, ai.title 项目名称, ai.release_date 发布时间, ai.url 链接地址, ai.module 模块, ai.have_supplementary 是否存在补充公告 '
            f'from announcement_info ai '
            f'left join announcement_detail ad on ai.id = ad.info_id '
            f'where ai.release_timestamp between {math.ceil(release_start_time.timestamp())} and {math.ceil(release_end_time.timestamp())}')

        if bid_max_amount.strip() != '':
            sql += f' and bid_amount_max <= {bid_max_amount}'

        if monitor_part.strip() != '':
            sql += f' and bid_monitor_org like "%{monitor_part}%"'

        if self.module != 0:
            sql += f' and module = {self.module}'

        print("sql:", sql)

        data = self.db.query(sql)

        if len(data) == 0:
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            self.resize_to_center(200, 100)
            return

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        self.tableWidget.setHorizontalHeaderLabels(data[0].keys())

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.tableWidget.verticalHeader().setVisible(False)  # 水平方向的表头
        # self.tableWidget.horizontalHeader().setVisible(False)  # 垂直方向的表头

        i = 0
        j = 0

        for row in data:
            for colName in row:
                value = row[colName]

                if colName == "链接地址":
                    value = GLOBAL_URI + value
                elif colName == "模块":
                    for enum in DataModule:
                        if enum.value['code'] == value:
                            value = enum.value['label']
                            break

                self.tableWidget.setItem(i, j, QTableWidgetItem(value))
                j += 1
            i += 1
            j = 0

        self.resize_to_center(1000, 600)

    def change_data_module(self, index):
        """
        工程类别选项发生改变时，重新渲染数据
        :return:
        """
        self.module = index
        selected_text = self.sender().currentText()
        selected_value = self.sender().currentData()
        print('渲染数据类别：', selected_text)
        print('渲染数据值：', selected_value)

    def update_data(self):
        """
        爬取最新的目标工程分类数据
        :return:
        """
        print("爬取最新的目标工程分类数据")

        # todo 根据self.module爬取不同类型数据
        spider_data(self.db, DataModule.HOUSE_BUILDING.value)

    # def closeEvent(self, event, **kwargs):
    #     reply = QMessageBox.question(self, 'Message',
    #                                  "Are you sure to quit?", QMessageBox.Yes |
    #                                  QMessageBox.No, QMessageBox.No)
    #
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def resize_to_center(self, *args):
        """
        将窗口移动到屏幕中央
        :param args: 窗口宽度 和 高度
        :return:
        """
        # 调整窗口大小
        self.resize(*args)

        # 获取屏幕的宽度和高度
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        # 获取窗口的宽度和高度
        window_width = self.geometry().width()
        window_height = self.geometry().height()

        # 计算窗口在屏幕中央的坐标
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # 将窗口移动到屏幕中央
        self.move(x, y)


def main(db_connect):
    app = QApplication(sys.argv)
    ex = window(db_connect)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    dbConnect = SqliteOperator('../storage/transactionInfo')
    init_db_struct(dbConnect)
    main(dbConnect)
