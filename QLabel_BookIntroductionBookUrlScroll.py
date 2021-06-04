from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QFont, QPainter, QColor


class QLabel_BookIntroductionBookUrlScroll(QLabel):
    def __init__(self, bookUrl: str):
        super().__init__()
        self.bookUrl = bookUrl
        self.setMinimumSize(200, 20)
        self.setMaximumSize(200, 20)
        self.newX = 10
        self.t = QTimer()
        self.font = QFont("'Microsoft YaHei", 9)
        self.t.timeout.connect(self.changeTxtPosition)

    def changeTxtPosition(self):
        if not self.parent().isVisible():
            # 如果parent不可见，则停止滚动，复位
            self.t.stop()
            self.newX = 10
            return
        if self.textRect.width() + self.newX > 0:
            # 每次向前滚动5像素
            self.newX -= 5
        else:
            self.newX = self.width()
        self.update()

    # 用drawText来绘制文字，不再需要setText，重写
    def setText(self, s):
        self.bookUrl = s

        # 滚动起始位置设置为10,留下视觉缓冲
        # 以免出现 “没注意到第一个字是什么” 的情况
        self.newX = 10
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.font)
        # 设置透明颜色
        painter.setPen(QColor('transparent'));

        # 以透明色绘制文字，来取得绘制后的文字宽度
        self.textRect = painter.drawText(
            QRect(0, -7, self.width(), 35),
            Qt.AlignCenter,
            self.bookUrl)

        if self.textRect.width() > self.width():
            # 如果绘制文本宽度大于控件显示宽度，准备滚动：
            painter.setPen(QColor(71, 145, 255, 255))
            painter.drawText(
                QRect(self.newX, -7, self.textRect.width(), 35),
                Qt.AlignCenter,
                self.bookUrl)
            # 每150ms毫秒滚动一次
            self.t.start(150)
        else:
            # 如果绘制文本宽度小于控件宽度，不需要滚动，文本居中对齐
            painter.setPen(QColor(71, 145, 255, 255))
            self.textRect = painter.drawText(
                QRect(0, -7, self.width(), 35),
                Qt.AlignCenter,
                self.bookUrl)
            self.t.stop()
