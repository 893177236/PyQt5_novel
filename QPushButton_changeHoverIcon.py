# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QEvent, QFileInfo
from PyQt5.QtGui import QIcon


class QPushButton_changeHoverIcon(QPushButton):
    def __init__(self):
        super().__init__()
        self.hover_config = {
            "add_to_bookshelf": {
                "default": "./Resource/icon/addToBookShelf.png",
                "hover": "./Resource/icon/addToBookShelf_w.png"
            },
            "open_book_file": {
                "default": "./Resource/icon/file.png",
                "hover": "./Resource/icon/file_w.png"
            },
            "del_from_download_layout": {
                "default": "./Resource/icon/delete.png",
                "hover": "./Resource/icon/delete_w.png"
            }
        }

    def enterEvent(self, a0: QEvent) -> None:
        self.iconToChange()

    def leaveEvent(self, a0: QEvent) -> None:
        self.iconToResume()

    def iconToChange(self):
        self.setIcon(QIcon(QFileInfo(self.getBtnHoverImagePath()).absoluteFilePath()))

    def iconToResume(self):
        self.setIcon(QIcon(QFileInfo(self.getBtnDefaultImagePath()).absoluteFilePath()))

    def getBtnHoverImagePath(self) -> str:
        current_btn: str = self.property("currentBtn")
        image_path = self.hover_config[current_btn]["hover"]
        return image_path

    def getBtnDefaultImagePath(self) -> str:
        current_btn: str = self.property("currentBtn")
        image_path = self.hover_config[current_btn]["default"]
        return image_path
