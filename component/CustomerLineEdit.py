from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QEvent, Qt


class CustomWidget(QLineEdit):
    def __init__(self, pressed_func=None, parent=None):
        super().__init__(parent)
        self.pressedFunc = pressed_func

    def event(self, event):
        if event.type() == QEvent.KeyPress:
            key_event = event
            if key_event.key() == Qt.Key_Escape:
                print("Escape key pressed")
            elif key_event.key() == Qt.Key_Return:
                self.pressedFunc()
            # 处理其他按键事件
            pass

        return super().event(event)
