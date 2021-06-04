# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QFrame
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QFileInfo
from PyQt5.QtGui import QFont, QIcon
from ui.chapterList import Ui_widget_chapterList
from QMessageBox_showMsg import QMessageBox_showMsg
import User
from log import Logger

log = Logger().getlog()


class QWidget_chapterList(QWidget, Ui_widget_chapterList):
    breakSignal_sendNeedRepairChapter = pyqtSignal(dict, str, int, object,int,int,int)

    def __init__(self, num: int, frame_image: QFrame):
        super().__init__()
        self.__need_repair_dict = {}
        self.setWindowIcon(QIcon(QFileInfo("./Resource/favicon.ico").absoluteFilePath()))
        self.serialNumber = self.__getSerialNumber(num=num)
        self.frame_image = frame_image
        if self.serialNumber is None:
            log.warning("当前书架serialNumber不存在,当前num%d" % num)
            return
        self.setupUi(self)
        self.initCss()
        self.checkBox_all_check.setEnabled(False)
        self.checkBox_all_check.clicked.connect(self.__on_allCheck_clicked)
        self.btn_ok.clicked.connect(self.__on_returnCheckNeedRepairChapterList_clicked)
        self.btn_cancle.clicked.connect(lambda: self.close())
        log.info("启动显示章节列表")
        log.info(f"当前书籍serialNumber{self.serialNumber}")

        bookChapterList = self.__getBookChapterList()
        for i in bookChapterList:
            # log.info(i[0])
            self.__addBookChapterList(bookSourceName=i[0])
        self.checkBox_all_check.setEnabled(True)

    def __on_returnCheckNeedRepairChapterList_clicked(self):
        self.selectChecked()
        isSelect = self.getCheckNeedRepairDict()
        isAutoRepair = 1 if self.checkBox_check_auto.isChecked() else 0
        if (len(isSelect) == 0) and (self.checkBox_check_auto.isChecked() == False):
            QMessageBox_showMsg(text="请选择需要修复的章节", icon="").makeSure()
        else:
            log.info("选择的章节" + str(isSelect))
            bookInfo = self.__getBookRule()
            bookUrl = bookInfo[0]
            bookRule = bookInfo[1]
            log.info("主页:%s,启用规则:%s" % (bookUrl, bookRule))

            self.breakSignal_sendNeedRepairChapter.emit(isSelect,
                                                        bookUrl,
                                                        bookRule,
                                                        self.frame_image,
                                                        self.spinBox_delay_time.value(),
                                                        self.serialNumber,
                                                        isAutoRepair)
            self.close()

    def __on_allCheck_clicked(self):
        check_state = Qt.Checked if self.checkBox_all_check.isChecked() else Qt.Unchecked
        for row in range(self.listWidget.count()):
            item = self.listWidget.item(row)
            item.setCheckState(check_state)
            if item.checkState() == Qt.Checked:
                self.addCheckNeedRepairDict(row=row, chapterName=item.text())
            else:
                self.delCheckNeedRepairDict(row=row)

    def __addBookChapterList(self, bookSourceName: str):
        item = QListWidgetItem()
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        item.setSizeHint(QSize(200, 50))
        item.setText(bookSourceName)
        item.setFont(QFont("Microsoft YaHei", 9))
        item.setCheckState(Qt.Unchecked)
        self.listWidget.addItem(item)
        self.update()

    def initCss(self):
        self.spinBox_delay_time.setStyleSheet(
            """
            /*spinbox 抬起样式*/
    QDateTimeEdit::up-button,QTimeEdit::up-button,QDoubleSpinBox::up-button,QSpinBox::up-button {subcontrol-origin:border;
        subcontrol-position:right;
        image: url(./Resource/icon/Icon_f_add.png);
        width: 20px;
        height: 20px;				
    }
    QDateTimeEdit::down-button,QTimeEdit::down-button,QDoubleSpinBox::down-button,QSpinBox::down-button {subcontrol-origin:border;
        subcontrol-position:left;
        image: url(./Resource/icon/Icon_f_reduce.png);
        width: 20px;
        height: 20px;
    }
    /*按钮按下样式*/
    QDateTimeEdit::up-button:pressed,QTimeEdit::up-button:pressed,QDoubleSpinBox::up-button:pressed,QSpinBox::up-button:pressed{subcontrol-origin:border;
        subcontrol-position:right;
        image: url(./Resource/icon/Icon_f_add_click.png);
        width: 20px;
        height: 20px;		
    }
     
    QDateTimeEdit::down-button:pressed,QTimeEdit::down-button:pressed,QDoubleSpinBox::down-button:pressed,QSpinBox::down-button:pressed{
        subcontrol-position:left;
        image: url(./Resource/icon/Icon_f_reduce_click.png);
        width: 20px;
        height: 20px;
    }
            """)

    def __getBookChapterList(self) -> list:
        user = User.UserSql()
        return user.selectBookShelfBookChapters(serialNumber=self.serialNumber)

    def __getBookRule(self):  # 获取该书籍主页和启用的规则
        user = User.UserSql()
        return user.selectBookShelfBookUrlAndRule(serialNumber=self.serialNumber)

    def __getSerialNumber(self, num: int) -> int:
        user = User.UserSql()
        return user.selectBookShelfSerialNumber(bookNums=num)[0]

    def getCheckNeedRepairDict(self) -> dict:
        return self.__need_repair_dict

    def addCheckNeedRepairDict(self, row: int, chapterName: str):
        self.__need_repair_dict[row] = f"{chapterName}"

    def delCheckNeedRepairDict(self, row: int):
        if row in self.__need_repair_dict:
            self.__need_repair_dict.pop(row)

    def selectChecked(self):
        for row in range(self.listWidget.count()):
            item = self.listWidget.item(row)
            if item.checkState() == 2:
                self.addCheckNeedRepairDict(row=row, chapterName=item.text())
            else:
                self.delCheckNeedRepairDict(row=row)
