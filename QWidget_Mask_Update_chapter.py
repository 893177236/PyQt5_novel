# -*- coding: utf-8 -*-
from typing import Union

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from random import choice
from log import Logger
log = Logger().getlog()

class QWidget_Mask_Update_chapter(QWidget):  # 遮罩层,书架书籍更新使用
    label_overlay: Union[QLabel, QLabel]

    def __init__(self,parent=None, gif:list=["./Resource/bookupdate_new_1s.gif", "./Resource/bookupdate_new_2s.gif",
                        "./Resource/bookupdate_new_3s.gif"]):
        super().__init__(parent)
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置透明
        self.gif = gif
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet('background:rgba(0,0,0,102);')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.add_btn()

    def show(self):
        """重写show，设置遮罩大小与parent一致
        """
        if self.parent() is None:
            log.info("遮罩没有父亲，关闭")
            self.close()
            return
        parent_rect = self.parent().geometry()
        log.info(f"父窗口宽：{parent_rect.width()},高：{parent_rect.height()}")
        self.setGeometry(0, 0, parent_rect.width(), parent_rect.height())
        super().show()

    def add_btn(self):
        overlay_path = choice(self.gif)

        self.label_overlay = QLabel(self)
        self.label_overlay.setMinimumSize(105, 155)
        self.label_overlay.setMaximumSize(105, 155)
        label_overlay_movie = QMovie(overlay_path)

        # label_overlay_movie.setScaledSize(QSize(105,155))

        label_overlay_movie.start()
        self.label_overlay.setMovie(label_overlay_movie)
        self.label_overlay.setScaledContents(True)
