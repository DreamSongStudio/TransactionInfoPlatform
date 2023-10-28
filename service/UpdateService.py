import threading

from PyQt5.QtGui import QIcon, QPixmap

import config.global_var as gv

from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QMessageBox
from main import spider_data
from utils.SqliteOperator import SqliteOperator


class MonitorUpdateService(QThread):
    """
    监听更新服务信号的线程
    这里采取 监听 - 发出信号 - 实际操作 的三层传递结构，来保证UI的操作活性
    """

    def __init__(self, target_modules: list, db_connect: SqliteOperator):
        super().__init__()
        self.targetModules = target_modules
        self.db = db_connect

    def run(self):
        print("数据更新服务监控")
        worker = UpdateService(self.targetModules, self.db)
        worker.finished.connect(self.handle_finished)  # 连接任务完成信号到槽函数
        worker.progress.connect(self.handle_progress)  # 连接进度信号到槽函数
        worker.run()

    def handle_finished(self):
        icon = QIcon("../imgs/菠萝.svg")
        messageBox = QMessageBox()
        messageBox.setWindowTitle("更新结果")
        messageBox.setIconPixmap(QPixmap("../imgs/logo1.jpg"))
        messageBox.setStandardButtons(QMessageBox.Yes)
        messageBox.setWindowIcon(icon)

        if gv.get_value("UPDATE_DATA_COUNT") > 0:
            messageBox.setText(f"更新完成，发现{gv.get_value('UPDATE_DATA_COUNT')}条新数据")
        else:
            messageBox.setText(f"未发现新数据")

        messageBox.exec_()

        # 初始化全局参数
        gv.set_value("UPDATE_DATA_COUNT", 0)

    def handle_progress(self, value):
        pass


class UpdateService(QObject):
    """
    更新数据的PyQt信号线程
    """
    finished = pyqtSignal()     # 自定义信号，用于通知任务完成
    progress = pyqtSignal(int)  # 自定义信号，用于通知进度

    def __init__(self, target_modules: list, db_connect: SqliteOperator):
        super().__init__()
        self.targetModules = target_modules
        self.db = db_connect

    def set_target_modules(self, target_modules):
        self.targetModules = target_modules

    def run(self):
        print(f"准备创建更新服务，扫描模块：{self.targetModules}")
        t = UpdateServiceImpl(self.targetModules, self.db)
        t.start()

        while not gv.get_value("UPDATE_DATA_FINISHED"):
            QThread.msleep(500)
            # 对外发送信号
            self.progress.emit(gv.get_value("UPDATE_DATA_COUNT"))

        self.finished.emit()


class UpdateServiceImpl(threading.Thread):
    """
    更新数据的实际线程
    """
    def __init__(self, target_modules: list, db_connect: SqliteOperator):
        threading.Thread.__init__(self)
        self.targetModules = target_modules
        self.db = db_connect

    def run(self):
        for module in self.targetModules:
            spider_data(self.db, module)
        gv.set_value("UPDATE_DATA_FINISHED", True)

