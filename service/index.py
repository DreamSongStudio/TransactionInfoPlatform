import math
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime
from component.CustomerLineEdit import CustomWidget
from main import spider_data, init_db_struct
from service.styles import header_labels_style, option_button_style, table_even_style, table_odd_style
from utils.SqliteOperator import SqliteOperator
from utils.Common import GLOBAL_URI
from models.Constant import DataModule


class window(QWidget):
    def __init__(self, db_connect: SqliteOperator, parent=None):
        super(window, self).__init__(parent)
        self.resize_to_center(1440, 960)
        self.monitorPartEdit = None
        self.bidMaxAmountEdit = None
        self.releaseTimeStart = None
        self.releaseTimeEnd = None
        self.moduleSelect = None
        self.tableWidget = None

        # 设置初始类型为0
        self.module = 0

        # 设置数据库对象
        self.db = db_connect

        self.setWindowTitle("招投标交易信息一览")

        self.searchGrid = QGridLayout()
        self.optionsArea = QGridLayout()

        self.init_search_layout()
        self.init_options_area()
        self.init_data_layout()

        dataViewGrid = QGridLayout()
        dataViewGrid.addLayout(self.searchGrid, 0, 0)
        dataViewGrid.addLayout(self.optionsArea, 0, 1)
        dataViewGrid.addWidget(self.tableWidget, 5, 0, 1, 2)
        self.setLayout(dataViewGrid)


        # self.search_option()

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

        self.releaseTimeEnd.setDate(default_date)
        self.releaseTimeStart.setDate(default_date.addDays(-7))


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
        # searchButton.setStyleSheet(option_button_style)
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        searchButton.setSizePolicy(size_policy)

        img_log_label = QLabel()
        pixmap = QPixmap("../imgs/logo1.jpg")  # 替换为你的图像文件路径
        img_log_label.setPixmap(pixmap)

        self.optionsArea.addWidget(updateDataButton, 0, 0, 1, 1)
        self.optionsArea.addWidget(searchButton, 1, 0, 2, 1)
        self.optionsArea.addWidget(img_log_label, 0, 2, 3, 10)

    def init_data_layout(self):
        """
        渲染数据展示表格
        :return:
        """
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(len(header_labels_style.keys()))
        # 设置水平表头标签

        self.tableWidget.setHorizontalHeaderLabels(header_labels_style.keys())
        # 设置每列固定宽度
        for column_index in range(self.tableWidget.columnCount()):
            header_item = self.tableWidget.horizontalHeaderItem(column_index)
            column_name = header_item.text()
            print(f'给第{column_index}列：{column_name}，设置宽度：{header_labels_style[column_name]["width"]}')
            self.tableWidget.setColumnWidth(column_index, header_labels_style[column_name]['width'])

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
            f'select ai.project_no 项目编号, '
            f'       ad.bid_amount_max "最高限价(万元)", '
            f'       ai.title 项目名称, '
            f'       ai.release_date 发布时间, '
            f'       ad.bid_monitor_org 监管机构, '
            f'       ai.url 链接地址, '
            f'       ai.module 模块 '
            f'from announcement_info ai '
            f'left join announcement_detail ad on ai.id = ad.info_id '
            f'where ai.release_timestamp between {math.ceil(release_start_time.timestamp())} and {math.ceil(release_end_time.timestamp())} ')

        sql += f' and bid_amount_max <= {bid_max_amount}' if bid_max_amount.strip() != '' else ''

        sql += f' and bid_monitor_org like "%{monitor_part}%"' if monitor_part.strip() != '' else ''

        sql += f' and module = {self.module}' if self.module != 0 else ''

        sql += ' order by ai.id desc'

        print("sql:", sql)

        data = self.db.query(sql)
        if len(data) == 0:
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(len(header_labels_style.keys()))
            self.tableWidget.setHorizontalHeaderLabels(header_labels_style.keys())
            return

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        columns = list(data[0].keys())
        self.tableWidget.setHorizontalHeaderLabels(columns)
        # 设置水平表头标签样式
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.tableWidget.verticalHeader().setVisible(False)  # 水平方向的表头
        # self.tableWidget.horizontalHeader().setVisible(False)  # 垂直方向的表头

        i = 0
        j = 0

        for row in data:
            for colName in row:
                value = str(row[colName]) if row[colName] else ""

                if colName == "链接地址":
                    value = GLOBAL_URI + value
                elif colName == "模块":
                    for enum in DataModule:
                        if enum.value['code'] == int(value):
                            value = enum.value['label']
                            break
                item = QTableWidgetItem(value)
                item.setToolTip(value)
                if i % 2 == 0:
                    item.setBackground(QColor(129, 219, 213))
                self.tableWidget.setItem(i, j, item)
                j += 1
            i += 1
            j = 0

        # 重新渲染数据后固定列宽度
        # self.tableWidget.resizeColumnsToContents()
        for column_index in range(self.tableWidget.columnCount()):
            self.tableWidget.horizontalHeader().setSectionResizeMode(column_index, QHeaderView.Fixed)

    def change_data_module(self, index):
        """
        工程类别选项发生改变时，重新渲染数据
        :return:
        """
        self.module = index
        selected_text = self.sender().currentText()
        selected_value = self.sender().currentData()
        self.search_option()

    def update_data(self):
        """
        爬取最新的目标工程分类数据
        :return:
        """
        print("爬取最新的目标工程分类数据")
        count = 0
        selected_options = []  # 存储选项的状态

        def get_checkboxes(layout):
            checkboxes = []
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if isinstance(item.widget(), QCheckBox):
                    checkboxes.append(item.widget())
                elif isinstance(item.layout(), QLayout):
                    checkboxes.extend(get_checkboxes(item.layout()))
            return checkboxes

        def select(checked):
            nonlocal count
            count = count - 1 if not checked else count + 1
            select_all_checkbox.setChecked(True) if count == len(DataModule) - 1 else select_all_checkbox.setChecked(False)

        def select_all_changed(checked):
            nonlocal count
            for item in get_checkboxes(layout):
                item.setChecked(checked)
            count = len(DataModule) - 1 if checked else 0

        # 创建窗口
        dialog = QDialog(self)
        dialog.setWindowTitle("更新数据模块")
        dialog.resize(200, 100)

        # 创建布局并添加部件
        layout = QVBoxLayout()
        select_all_checkbox = QCheckBox(DataModule.ALL.value['label'])
        select_all_checkbox.clicked.connect(select_all_changed)
        layout.addWidget(select_all_checkbox)

        for v in DataModule:
            box = QCheckBox(v.value['label'])
            box.clicked.connect(select)
            layout.addWidget(box) if v.value['code'] != 0 else None
            selected_options.append(box)  # 将选项添加到列表中

        # 创建确认按钮
        button = QPushButton("更新")
        button.clicked.connect(dialog.accept)
        layout.addWidget(button)

        dialog.setLayout(layout)

        # 显示弹出窗口
        if dialog.exec_() == QDialog.Accepted:
            # 获取选择的选项
            for option in selected_options:
                if option.isChecked():
                    print(option.text() + " selected")
                    for v in DataModule:
                        if option.text() == v.value["label"]:
                            spider_data(self.db, v.value)
                            break

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
