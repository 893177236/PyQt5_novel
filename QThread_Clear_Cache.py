# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, QThread
import os
import User
from log import Logger
log = Logger().getlog()

class QThread_Clear_Cache(QThread):
    breakSignal_setLabel = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        useful_pic = self.selectUsefulImageCache()
        useful_pic_size = 0
        log.info(str(useful_pic))
        useful_pic_num = len(useful_pic)
        current_path = os.getcwd().replace("\\", "/")
        cache_path = current_path + "/Resource/Cache"
        cache_images = os.walk(top=cache_path, topdown=False)
        for root, dirs, files in cache_images:
            for file in files:
                if cache_path + f"/{file}" in useful_pic:
                    log.info(f"不删除{file}")
                    useful_pic_size += os.path.getsize(filename=cache_path + f"/{file}")
                else:
                    try:
                        os.remove(path=cache_path + f"/{file}")
                    except FileNotFoundError:
                        log.info(f"{cache_path}不存在")
        self.breakSignal_setLabel.emit(
            "<font color=\"orange\">0</font> Useless Pictures(<font color=\"red\">0B</font>)",
            f"& <font color=\"#01DF3A\">{useful_pic_num}</font> "
            f"Useful Pictures(<font color=\"#01DF3A\">{self.calculate_file_size(Byte=useful_pic_size)}</font>)")

    @staticmethod
    def selectUsefulImageCache() -> list:
        user = User.UserSql()
        images_path = user.selectCacheImages()
        images_path_list = [image[0] for image in images_path]
        images_path_list_new = list(filter(lambda x: "Resource/noCover.jpeg" not in x, images_path_list))
        return images_path_list_new

    @staticmethod
    def calculate_file_size(Byte: int) -> str:  # 计算文件确定大小
        if 1024 <= Byte < 1022976:  # KB
            new_size = f"{round(Byte / 1024, 2)}KB"
        elif 1022976 <= Byte < 1047527424:  # MB
            new_size = f"{round(Byte / 1024 / 1024, 2)}MB"
        elif 1047527424 <= Byte < 1072668082176:  # GB
            new_size = f"{round(Byte / 1024 / 1024 / 1024, 2)}GB"
        elif Byte >= 1072668082176:  # TB
            new_size = f"{round(Byte / 1024 / 1024 / 1024 / 1024, 2)}TB"
        else:
            new_size = f"{Byte}B"
        return new_size
