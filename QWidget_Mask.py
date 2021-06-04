from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

class QWidget_Mask(QWidget):  # 遮罩层
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet('background:rgba(0,0,0,102);')
        self.setAttribute(Qt.WA_DeleteOnClose)

    def show(self):
        """重写show，设置遮罩大小与parent一致
        """
        if self.parent() is None:
            self.close()
            return
        parent_rect = self.parent().geometry()
        self.setGeometry(0, 0, parent_rect.width(), parent_rect.height())
        super().show()