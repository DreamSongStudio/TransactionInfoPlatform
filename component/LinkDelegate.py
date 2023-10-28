from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QStyledItemDelegate, QStyle
from PyQt5.QtGui import QColor, QDesktopServices
from PyQt5.QtCore import Qt, QUrl


class LinkDelegate(QStyledItemDelegate):
    """
    自定义委托类，用以丰富table单元格的功能
    """
    def createEditor(self, parent, option, index):
        return None  # 禁用编辑器

    def paint(self, painter, option, index):
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        item = index.data(Qt.DisplayRole)
        url = index.data(Qt.UserRole)

        if isinstance(item, str) and url is not None:
            painter.save()

            # 绘制带下划线的文本
            painter.setPen(QColor(0, 0, 255))
            painter.drawText(option.rect, Qt.AlignHCenter | Qt.AlignVCenter, item)
            painter.setBackground(QColor(129, 219, 213))
            painter.restore()
        else:
            super().paint(painter, option, index)  # 处理其他列的绘制

    def editorEvent(self, event, model, option, index):
        if event.type() == event.MouseButtonRelease and event.button() == Qt.LeftButton:
            url = index.data(Qt.UserRole)

            if url is not None:
                QDesktopServices.openUrl(QUrl(url))

        return False

