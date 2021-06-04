# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFocusEvent, QMouseEvent, QCursor, QPixmap
from ui.findResponse import Ui_bookIntroduction
from QLabel_BookIntroductionBookUrlScroll import QLabel_BookIntroductionBookUrlScroll
import User
from log import Logger
log = Logger().getlog()

class QWidget_BookIntroduction(QWidget, Ui_bookIntroduction):  # 书籍信息
    label_sourceUrl_right: QLabel_BookIntroductionBookUrlScroll
    breakSignal_showReader = pyqtSignal(int, object)

    def __init__(self, bookNums: int, label_process: QLabel):
        super().__init__()
        self.bookNums = bookNums
        self.label_process = label_process
        self.m_flag = None  # 鼠标移动
        self.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet("""
        QPushButton#btn_toread{
            color: #0099CC;
            background: transparent;
            border: 2px solid #0099CC;
            border-radius: 6px;
            border: none;
            color: white;
            padding: 6px 12px;
            text-align: center;
            font-size: 15px;
            margin: 4px 2px;
            text-decoration: none;
            text-transform: uppercase;
            background-color: white;
            color: black;
            border: 2px solid #008CBA;
        }
        QPushButton#btn_toread:hover{
            background-color: #008CBA;
            color: white;
        }
        QPushButton#btn_toread:pressed{
            padding-left: 16px;
            padding-top: 9px;
        }
        QPushButton#btn_image{
            border-radius:6px;
        }
        """)
        self.initSetting()

    def setLabelControl(self, bookUrl: str):
        self.label_sourceUrl_right = QLabel_BookIntroductionBookUrlScroll(bookUrl=bookUrl)
        self.hlayout_sourceUrl.addWidget(self.label_sourceUrl_right)

    def initSetting(self) -> None:
        user = User.UserSql()
        book_info = user.selectBookShelfBookInfo(bookNums=self.bookNums)

        # log.info(bookInfo)
        if book_info is None:
            log.info("没有检索到书籍信息")
            self.deleteLater()
        else:
            book_image = book_info[0]
            book_name = book_info[1]
            book_progress = book_info[2]
            book_path = book_info[3]
            book_author = book_info[5]
            book_status = book_info[6]
            book_latest_chapter = book_info[7]
            book_latest_update_time = book_info[8]
            book_intro = book_info[9]

            book_source_name = book_info[10]
            book_url = book_info[11]
            book_serial_number = book_info[13]

            log.info(f"书籍图片地址：{book_image}，书名：{book_name}，进度：{book_progress}，本地地址：{book_path}")
            log.info(f"作者：{book_author}，状态：{book_status}，最新章节：{book_latest_chapter}，更新时间：{book_latest_update_time}")
            self.btn_image.setStyleSheet(f"border-image:url('{book_image}')")
            self.label_bookName_2.setText(book_name)
            self.label_bookProgress_2.setText(str(book_progress))
            if book_progress > 0:
                self.btn_toread.setText("继续阅读")
            self.label_bookAuthor_2.setText(book_author)
            self.label_bookStatus_2.setText(book_status)
            self.label_latestChapter_2.setText(book_latest_chapter)
            self.label_latestUpdateTime_2.setText(book_latest_update_time)
            self.label_bookIntro_2.setText(book_intro)
            self.label_sourceName_right.setText(book_source_name)
            # self.label_sourceUrl_right.setWordWrap(True)
            # self.label_sourceUrl_right.setText(bookUrl)
            self.setLabelControl(bookUrl=book_url)

            log.info("设置点击事件")

            self.btn_toread.clicked.connect(lambda: self.SignalCall(book_serial_number))

    def SignalCall(self, bookSerialNumber: int):
        log.info(f"当前特定书籍号：{bookSerialNumber}")
        self.breakSignal_showReader.emit(int(bookSerialNumber), self.label_process)
        self.setFocus()

    def focusOutEvent(self, a0: QFocusEvent) -> None:
        if not self.btn_toread.hasFocus():
            self.deleteLater()

    def focusInEvent(self, a0: QFocusEvent) -> None:
        log.info("焦点进入")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            # self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标
            self.setCursor(QCursor(QPixmap(":/cursor/Cur/No_Disponible.cur"), 0, 0))

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position)  # 更改窗口位置
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.m_flag = False
        # self.setCursor(QCursor(Qt.ArrowCursor))
        self.setCursor(QCursor(QPixmap(":/cursor/Cur/normal.cur"), 0, 0))
