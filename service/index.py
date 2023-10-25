import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from component.CustomerLineEdit import CustomWidget
from models.Constant import DataModule


class window(QWidget):

    def __init__(self, parent=None):
        super(window, self).__init__(parent)
        # self.resize(200, 50)
        self.monitorPartEdit = None
        self.bidMaxAmountEdit = None
        self.releaseTimeStart = None
        self.releaseTimeEnd = None
        self.moduleSelect = None

        self.setWindowTitle("招投标交易信息一览")

        dataViewGrid = QGridLayout()
        self.searchGrid = QGridLayout()
        self.optionsArea = QGridLayout()

        self.init_search_layout()
        self.init_options_area()

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
        self.releaseTimeStart = QDateEdit()
        self.releaseTimeEnd = QDateEdit()

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
        release_start_time = self.releaseTimeStart.text()
        release_end_time = self.releaseTimeEnd.text()
        print(f'监管部门：{monitor_part}， 最高限价：{bid_max_amount}，发布时间：{release_start_time}到{release_end_time}')

    def change_data_module(self, index):
        """
        工程类别选项发生改变时，重新渲染数据
        :return:
        """
        selected_text = self.sender().currentText()
        selected_value = self.sender().currentData()
        print('渲染数据类别：', selected_text)

    def update_data(self):
        """
        爬取最新的目标工程分类数据
        :return:
        """
        print("爬取最新的目标工程分类数据")


def main():
    app = QApplication(sys.argv)
    ex = window()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
