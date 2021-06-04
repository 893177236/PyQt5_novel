# -*- coding: utf-8 -*-
import sqlite3
import os
from log import Logger

log = Logger().getlog()


class UserSql:
    def __init__(self):
        self.con = sqlite3.connect("./user.db")
        self.cur = self.con.cursor()
        self.path = os.getcwd().replace("\\", "/")
        self.saveFilePath = self.path + "/Download"
        self.progressNum = 0
        self.parallelTasks = 0
        self.downloadFinishMusicPath = self.path + '/Resource/video/1.wav'

    def __del__(self):
        self.con.commit()
        self.con.close()

    def checkDefaultTable(self) -> None:  # 检索数据库状态
        self.checkUser()
        self.checkBookShelf()
        self.checkDownload()

    def checkUser(self) -> None:  # 检索用户设置布局数据
        sql = "select * from sqlite_master where type = 'table' and name='user';"
        result = self.cur.execute(sql)
        if result.fetchone() is None:  # 不存在表就创建
            log.info("错误！不存在user表，创建")
            self.createUserInfoTable()
            self.insertDefaultData()

    def checkBookShelf(self) -> None:  # 检索书架布局数据
        sql = "select * from sqlite_master where type = 'table' and name='bookshelf';"
        result = self.cur.execute(sql)
        if result.fetchone() is None:  # 不存在表就创建
            log.info("错误！不存在bookshelf表，创建")
            self.createBookShelfInfoTable()
            self.insertDefaultData()

    def checkDownload(self) -> None:  # 检索下载布局数据
        sql = "select * from sqlite_master where type = 'table' and name='download';"
        result = self.cur.execute(sql)
        if result.fetchone() is None:  # 不存在表就创建
            log.info("错误！不存在download表，创建")
            self.createDownloadInfoTable()
            self.insertDefaultData()

    def insertDefaultData(self) -> None:  # 创建用户默认数据

        sql = f"insert into user (id,saveFilePath,progressNum,parallelTasks,downloadFinishMusicPath)" \
              f"values (1,'{self.saveFilePath}',{self.progressNum}," \
              f"{self.parallelTasks},{self.downloadFinishMusicPath})"

        self.cur.execute(sql)
        # self.con.commit()  # 提交

    def insertReaderBookNormalInfo(self, currentPage: int,
                                   serialNumber: int,
                                   scrollTop: int):  # 添加书架某个书的阅读器的初始值
        sql = 'replace into reader(currentPage, serialNumber, scrollTop) ' \
              f'values ({currentPage},{serialNumber},{scrollTop})'
        self.cur.execute(sql)
        # self.con.commit()

    def insertBookShelfLayoutInfoSqlite(self,
                                        bookImage,
                                        bookName,
                                        bookProgress,
                                        bookPath,
                                        bookNums,
                                        bookAuthor,

                                        bookStatus,
                                        bookLatestChapter,
                                        bookLatestUpdateTime,
                                        bookIntro,
                                        bookSourceName,

                                        bookUrl,
                                        bookRule,
                                        bookSerialNumber
                                        ):  # 添加新的书架数据
        sql = f"""
        insert into bookshelf
         (                          
            bookImagePath,
            bookName,
            bookProgress,
            bookPath,
            bookNums,
            bookAuthor,
            bookStatus,
            bookLatestChapter,
            bookLatestUpdateTime,
            bookIntro,
            bookSourceName,
            bookUrl,
            bookRule,
            bookSerialNumber
        )
        values(
            '{bookImage}',
            '{bookName}',
             {bookProgress},
            '{bookPath}',
             {bookNums},
            '{bookAuthor}',
            '{bookStatus}',
            '{bookLatestChapter}',
            '{bookLatestUpdateTime}',
            '{bookIntro}',
            '{bookSourceName}',
            '{bookUrl}',
             {bookRule},
             {int(bookSerialNumber)}
        )
        """

        self.cur.execute(sql)
        # self.con.commit()

    def createUserInfoTable(self) -> None:  # 创建用户数据表
        sql = '''create table if not exists user 
            (
                id int primary key not null,
                saveFilePath text not null,
                progressNum int not null,
                parallelTasks int not null,
                downloadFinishMusicPath text not null
            );'''
        self.cur.execute(sql)
        # self.con.commit()  # 提交

    def createBookShelfInfoTable(self) -> None:  # 创建书架布局表
        sql = '''create table bookshelf
                (
                    bookImagePath text not null,
                    bookName      text not null,
                    bookProgress  real not null,
                    bookPath      text not null,
                    bookNums      int  not null
                );
            '''
        self.cur.execute(sql)
        # self.con.commit()

    def createDownloadInfoTable(self) -> None:  # 创建下载布局表
        sql = '''create table if not exists download
                (
                    taskBookImagePath text    not null,
                    taskBookName      text    not null,
                    taskCreateTime    text    not null,
                    taskFinishTime    text    not null,
                    taskProgress      int     not null,
                    taskStatusInfo    text    not null,
                    taskBtnStatus     integer not null,
                    taskBookPath      text    not null,
                    taskLine          int     not null
                );
                '''
        self.cur.execute(sql)
        # self.con.commit()

    def selectCacheImages(self) -> list:  # 检索缓存必须的图片
        sql = 'select taskBookImagePath from download;'
        result = self.cur.execute(sql)
        bookresult = result.fetchall()
        return bookresult

    def selectBookShelfImagePath(self):
        sql = 'select bookImagePath,bookSerialNumber from bookshelf;'
        result = self.cur.execute(sql)
        bookresult = result.fetchall()
        return bookresult

    def selectDownloadImagePath(self):
        sql = 'select taskBookImagePath,taskSerialNumber from download;'
        result = self.cur.execute(sql)
        bookresult = result.fetchall()
        return bookresult

    def updateBookShelfImagePath(self, imagePath: str, serialNumber: int):
        sql = f"update bookshelf set bookImagePath='{imagePath}' where bookSerialNumber={serialNumber};"
        self.con.execute(sql)
        # self.con.commit()  # 提交

    def updateDownloadImagePath(self, imagePath: str, serialNumber: int):
        sql = f"update download set taskBookImagePath='{imagePath}' where taskSerialNumber={serialNumber};"
        self.con.execute(sql)
        # self.con.commit()  # 提交

    def selectReadBookInfo(self, chapterSerialNumber: int) -> list:  # 检索阅读信息内容
        sql = f'select distinct chapterBookSerialNumber,chapterName,chapterContent ' \
              f'from bookinfo left join bookshelf where chapterSerialNumber={chapterSerialNumber} order by chapterSerialNumber;'
        result = self.cur.execute(sql)
        bookresult = result.fetchall()
        return bookresult

    def selectBookShelfLayout(self) -> list:  # 检索书架布局
        sql = 'select * from bookshelf order by  bookNums;'
        result = self.cur.execute(sql)
        bookresult = result.fetchall()
        log.info("检索书架布局%s" % (str(bookresult)))
        return bookresult

    def selectBookShelfBookSerialNumber(self) -> list:  # 获取书架所有书籍的serial
        sql = 'select bookSerialNumber from bookshelf;'
        result = self.cur.execute(sql)
        bookresult = result.fetchall()
        log.info("检索所有书籍的SeribalNumber%s" % (str(bookresult)))
        return bookresult

    def selectBookShelfBookInfo(self,
                                bookNums: int) -> list:  # 检索某个书籍
        sql = f'select * from bookshelf where bookNums={bookNums};'
        result = self.cur.execute(sql)
        bookresult = result.fetchone()
        # log.info(searchResult)
        return bookresult

    def selectBookReaderCurrentPage(self, serialNumber: int):  # 获取阅读器的读的书的当前page
        sql = f'select currentPage from reader where serialNumber={serialNumber}'
        result = self.cur.execute(sql)
        bookresult = result.fetchone()
        return bookresult

    def selectBookReaderScrollTop(self, serialNumber: int):  # 获取阅读器的读的书的当前scrolltop
        sql = f'select scrollTop from reader where serialNumber={serialNumber}'
        result = self.cur.execute(sql)
        bookresult = result.fetchone()
        return bookresult

    def selectBookShelfMaxBookNum(self) -> list:  # 检索书架中最大的一本书
        sql = 'select max(bookNums) from bookshelf;'
        result = self.cur.execute(sql)
        bookresult = result.fetchone()
        return bookresult

    def selectBookShelfSerialNumber(self, bookNums):  # 根据书num获取特定serial
        sql = f'select bookSerialNumber from bookshelf where bookNums={int(bookNums)}'
        result = self.cur.execute(sql)
        bookresult = result.fetchone()
        return bookresult

    def selectBookShelfBookChapters(self, serialNumber: int):  # 根据书serialNumber获取所有章节
        sql = f'select chapterName from bookinfo where chapterSerialNumber={int(serialNumber)}'
        result = self.cur.execute(sql)
        bookresult = result.fetchall()
        return bookresult

    def selectBookShelfBookUrlAndRule(self, serialNumber: int):  # 根据书serialNumber获取书架的书的主页和启用的规则
        sql = f'select bookUrl,bookRule from bookshelf where bookSerialNumber={int(serialNumber)};'
        result = self.cur.execute(sql)
        bookresult = result.fetchone()
        return bookresult

    def selectBookShelfChapterTotalNums(self, serialNumer):  # 检索某个书籍的章节数目
        sql = f'select count(chapterName) from bookinfo where chapterSerialNumber={serialNumer}'
        result = self.cur.execute(sql)
        book_chapter_total_nums = result.fetchone()
        return book_chapter_total_nums

    def selectBookShelfProgress(self, serialNum):  # 根据书serial获取进度
        sql = f'select bookProgress from bookshelf where bookSerialNumber={int(serialNum)}'
        result = self.cur.execute(sql)
        bookresult = result.fetchone()
        return bookresult

    def selectBookReaderMaxNum(self, serialNum: int) -> list:  # 检索该书籍最大的章节数
        sql = f'select max(ROWID) from bookinfo where chapterSerialNumber={int(serialNum)};'
        result = self.cur.execute(sql)
        bookresult = result.fetchone()
        return bookresult

    def selectBookInfoOriginalChapter(self, chapterSerialNumber: int):  # 检索本机书
        sql = f'select chapterName,chapterContent,chapterBookSerialNumber from bookinfo where chapterSerialNumber={chapterSerialNumber}'
        result = self.cur.execute(sql)
        bookresult = result.fetchall()
        return bookresult

    def selecDownloadLayout(self) -> list:  # 检索下载记录布局
        sql = 'select * from download order by  taskLine;'
        result = self.cur.execute(sql)
        bookresult = result.fetchall()
        # log.info(searchResult)
        return bookresult

    def selectHomeUrl(self) -> list:
        sql = """select  taskHomeUrl as url from download
                union
                select  bookUrl as url from bookshelf"""
        result = self.cur.execute(sql)
        bookresult = result.fetchall()
        return bookresult

    def selectUserInfo(self) -> dict:  # 检索用户数据

        sql = 'select saveFilePath,' \
              'progressNum,' \
              'parallelTasks,' \
              'downloadFinishMusicPath,' \
              'downloadTaskDelayTime,' \
              'searchProcessNum,' \
              'left_widget' \
              ' from user where id=1'

        result = self.cur.execute(sql)
        bookresult = result.fetchmany(3)

        savefilepath = bookresult[0][0]
        progressnum = bookresult[0][1]
        paralleltasks = bookresult[0][2]
        downloadfinishmusicpath = bookresult[0][3]
        downloadtaskdelaytime = bookresult[0][4]
        searchProcessNum = int(bookresult[0][5])
        left_widget = int(bookresult[0][6])
        log.info(
            f"User类检索的数据：{savefilepath}, {progressnum}, "
            f"{paralleltasks}, {downloadfinishmusicpath}, "
            f"{downloadtaskdelaytime},{searchProcessNum}"
            f"{left_widget}")
        return {
            "saveFilePath": savefilepath,
            "progressNum": progressnum,
            "parallelTasks": paralleltasks,
            "downloadFinishMusicPath": downloadfinishmusicpath,
            "downloadTaskDelayTime": downloadtaskdelaytime,
            "searchProcessNum": searchProcessNum,
            "left_widget": left_widget
        }

    def selectProcessNums(self) -> int:  # 获取进程数量
        sql = 'select progressNum from user where id=1;'
        result = self.cur.execute(sql)
        searchresult = result.fetchone()

        processnums = int(searchresult[0]) if searchresult else 1
        log.info(f"检索数据库中的进程数量:{processnums}")

        return processnums

    def selectDownloadTaskDelayTime(self) -> int:  # 获取下载延迟时间
        sql = 'select downloadTaskDelayTime from user where id=1;'
        result = self.cur.execute(sql)
        searchresult = result.fetchone()[0]

        return searchresult

    def selectParallelTasks(self) -> int:  # 获取并行任务数量
        sql = 'select parallelTasks from user where id=1;'
        result = self.cur.execute(sql)
        searchresult = result.fetchone()

        paralleltasks = int(searchresult[0]) if searchresult else 1
        log.info(f"检索数据库中的并行任务数量：{paralleltasks}")
        return paralleltasks

    def selectSaveFileLocation(self) -> str:  # 获取保存文件路径
        sql = 'select saveFilePath from user where id=1;'
        result = self.cur.execute(sql)
        searchresult = result.fetchone()
        savefilelocation = searchresult[0] if searchresult else searchresult
        log.info(f"检索数据库中的保存文件路径:{savefilelocation}")
        return savefilelocation

    def selectFinishDownloadMusicPath(self) -> str:
        sql = 'select downloadFinishMusicPath from user where id=1;'
        result = self.cur.execute(sql)
        searchresult = result.fetchone()
        finishdownloadnusicpath = searchresult[0] if searchresult else searchresult
        log.info(f"检索数据库中的提示音的路径:{finishdownloadnusicpath}")
        return finishdownloadnusicpath

    def selectComboboxSortChooseIndex(self) -> int:  # 检索多选框搜索排序
        sql = 'select sort_choose from search where id=1;'
        result = self.cur.execute(sql)
        search_result = result.fetchone()
        return search_result[0]

    def selectIsInBookInfoDatabase(self) -> list:
        sql = '''        select bookInfoSerial as serialNumber,
               bookName,
               bookAuthor,
               latestChapterName,
               bookUrl,
               totalChapters,
               sourcename,
               spaceSize
               from
        (select chapterSerialNumber as bookInfoSerial,
                count(*) as totalChapters,
                sum(length(chapterContent)) as spaceSize
        from bookinfo group by chapterSerialNumber),
        (select taskSerialNumber as downloadSerial,
               taskBookName as bookName,
               taskBookAuthor as bookAuthor,
               taskBookLatestChapter as latestChapterName,
               taskHomeUrl as bookUrl,
               taskBookSourceName as sourcename
        from download
        where  taskSerialNumber in (
        select distinct chapterSerialNumber as totalChapters
        from bookinfo group by chapterSerialNumber)) where bookInfoSerial=downloadSerial
        union
        select serialNumber,
               bookName,
               bookAuthor,
               latestChapterName,
               bookUrl,
               totalChapters,
               sourcename,
               spaceSize
        from
        (select chapterSerialNumber as bookInfoSerial,
                count(*) as totalChapters,
                sum(length(chapterContent)) as spaceSize
        from bookinfo group by chapterSerialNumber),
        (select bookSerialNumber as serialNumber,
               bookName as bookName,
               bookAuthor as bookAuthor,
               bookLatestChapter as latestChapterName,
               bookUrl as bookUrl,
               bookSourceName as sourcename
        from bookshelf
        where  bookSerialNumber in (select distinct chapterSerialNumber from bookinfo))
        where bookInfoSerial=serialNumber
        union
        select chapterSerialNumber as serialNumber,
               '未知书名' as bookName,
               '未知作者' as bookAuthor,
               chapterName as latestChapterName,
               '未知主页' as bookUrl,
               count(chapterBookSerialNumber) as totalChapters,
               '未知来源' as sourceName,
               sum(spaceSize) as spaceSize
        from (
            select chapterSerialNumber,
            chapterName,
            chapterBookSerialNumber,
            length(chapterContent) as spaceSize
            from bookinfo where chapterSerialNumber not in (
                select bookSerialNumber from bookshelf
            )order by chapterBookSerialNumber desc
        ) 
        group by chapterSerialNumber'''
        result = self.con.execute(sql)
        result_list = result.fetchall()
        return result_list

    def updateComboboxSortChooseIndex(self, index: int = 0) -> None:  # 更新多选框搜索排序下标
        sql = f'update search set sort_choose={index} where id=1;'
        self.con.execute(sql)
        # self.con.commit()  # 提交

    def updateUserInfo(self,
                       savefilepath: str = None,
                       progressnum: int = None,
                       paralleltasks: int = None,
                       downloadfinishmusicpath: str = None,
                       downloadtaskdelaytime: int = 3,
                       searchProcessNum: int = 1) -> None:  # 更新用户数据
        if savefilepath is None:
            savefilepath = self.saveFilePath
        if progressnum is None:
            progressnum = self.progressNum
        if paralleltasks is None:
            paralleltasks = self.parallelTasks
        if downloadfinishmusicpath is None:
            downloadfinishmusicpath = self.downloadFinishMusicPath
        log.info(
            f"User类将要更新的数据:{savefilepath}, {progressnum}, {paralleltasks}, {downloadfinishmusicpath}, {downloadtaskdelaytime}")
        sql = f"update user set saveFilePath ='{savefilepath}'," \
              f"progressNum={progressnum}," \
              f"parallelTasks={paralleltasks}," \
              f"downloadFinishMusicPath='{downloadfinishmusicpath}'," \
              f"downloadTaskDelayTime={downloadtaskdelaytime}," \
              f"searchProcessNum={searchProcessNum} " \
              "where id=1;"
        self.con.execute(sql)
        # self.con.commit()  # 提交

    def updateUserInfoLeftWidget(self, status: int):
        sql = f'update user set left_widget={status} where id=1;'
        self.con.execute(sql)
        # self.con.commit()

    def updateReaderConf(self, currentPage: int, serialNumber: int):
        sql = f'update reader set currentPage={currentPage} where serialNumber={serialNumber};'
        self.con.execute(sql)
        # self.con.commit()

    def updateReaderConfScrollTop(self, scrollTop: int, serialNumber: int):
        sql = f'update reader set scrollTop={scrollTop} where serialNumber={serialNumber};'
        self.con.execute(sql)
        # self.con.commit()

    def updateBookShelfLayoutInfo(self,
                                  bookNums: int) -> None:  # 更新书架界面布局
        sql = f'update bookshelf set bookNums=bookNums-1 where bookNums>{bookNums};'
        self.con.execute(sql)
        # self.con.commit()

    def updateBookShelfNewInfo(self,
                               bookLatestChapter: str,
                               bookLatestUpdateTime: str,
                               bookSerialNumber: int):  # 更新章节简介
        sql = "update bookshelf " \
              f"set bookLatestChapter='{bookLatestChapter}'," \
              f"bookLatestUpdateTime='{bookLatestUpdateTime}' " \
              f"where bookSerialNumber={bookSerialNumber};"
        self.con.execute(sql)
        # self.con.commit()

    def updateNewChapterInfo(self,
                             chapterContent: str,
                             chapterSerialNumber: int,
                             chapterBookSerialNumber: int
                             ):  # 修复书籍内容
        sql = f"update bookinfo set chapterContent='{chapterContent}' " \
              f"where chapterSerialNumber={int(chapterSerialNumber)} and chapterBookSerialNumber={int(chapterBookSerialNumber)}"
        self.con.execute(sql)
        # self.con.commit()

    def updateBookReaderProgress(self, progress: float, serialNum: int):  # 更新该书籍进度
        sql = f'update bookshelf set bookProgress={progress} where bookSerialNumber={serialNum}'
        self.con.execute(sql)
        # self.con.commit()

    def updateDownloadInfo(self, taskfinishtime: str, taskprogress: int, taskstatusinfo: str, taskbtnstatus: int,
                           taskserialNumber: int, taskprogresslabel: int):
        sql = f"update download " \
              f"set taskfinishtime='{taskfinishtime}'," \
              f"taskprogress={taskprogress}," \
              f"taskstatusinfo='{taskstatusinfo}'," \
              f"taskbtnstatus={taskbtnstatus}, " \
              f"taskProgressLabel={taskprogresslabel} " \
              f"where taskSerialNumber={taskserialNumber};"
        self.con.execute(sql)

    def insertDownloadLayoutInfo(self,
                                 taskBookImagePath: str,
                                 taskBookName: str,
                                 taskCreateTime: str,
                                 taskFinishTime: str,
                                 taskProgress: int,
                                 taskStatusInfo: str,
                                 taskBtnStatus: int,
                                 taskBookPath: str,
                                 taskLine: int,
                                 taskHomeUrl: str,
                                 taskWhichRule: int,
                                 taskProgressLabel: str,

                                 taskBookAuthor: str,
                                 taskBookStatus: str,
                                 taskBookIntro: str,
                                 taskBookSourceName: str,
                                 taskBookLatestChapter: str,
                                 taskLatestUpdateTime: str,
                                 taskSerialNumber: int  # 任务序列号
                                 ) -> None:  # 插入下载界面布局新数据
        sql = "insert into download " \
              "(taskBookImagePath, taskBookName, taskCreateTime, " \
              "taskFinishTime, taskProgress, taskStatusInfo, " \
              "taskBtnStatus, taskBookPath, taskLine, " \
              "taskHomeUrl, taskWhichRule, taskProgressLabel," \
              "taskBookAuthor,taskBookStatus,taskBookIntro," \
              "taskBookSourceName,taskBookLatestChapter,taskLatestUpdateTime," \
              "taskSerialNumber) values " \
              f"('{taskBookImagePath}', '{taskBookName}', '{taskCreateTime}', " \
              f"'{taskFinishTime}',{taskProgress}, '{taskStatusInfo}', " \
              f"{taskBtnStatus}, '{taskBookPath}', {taskLine}, " \
              f"'{taskHomeUrl}',{taskWhichRule},'{taskProgressLabel}'," \
              f"'{taskBookAuthor}','{taskBookStatus}','{taskBookIntro}'," \
              f"'{taskBookSourceName}','{taskBookLatestChapter}','{taskLatestUpdateTime}'," \
              f"{taskSerialNumber});"
        self.con.execute(sql)
        # self.con.commit()

    def insertChapterInfo(self, chapterName: str,
                          chapterContent: str,
                          chapterSerialNum: int,
                          chapterBookSerialNum: int):
        sql = f"insert into bookinfo" \
              f"(chapterName, chapterContent, chapterSerialNumber, chapterBookSerialNumber) values" \
              f"('{chapterName}','{chapterContent}',{chapterSerialNum},{chapterBookSerialNum});"
        self.con.execute(sql)


    def insertNewChapterInfo(self, chapterName: str, chapterContent: str, chapterSerialNumber: int):
        sql = "insert into bookinfo (" \
              "chapterName, chapterContent, chapterSerialNumber, chapterBookSerialNumber)" \
              f"VALUES ('{chapterName}','{chapterContent}',{chapterSerialNumber}," \
              f"(select ifnull(max(chapterBookSerialNumber),0) " \
              f"from bookinfo where chapterSerialNumber={chapterSerialNumber})+1);"
        self.con.execute(sql)
        # self.con.commit()

    def deleteDownloadLayoutInfo(self,
                                 row: int) -> None:  # 删除下载界面布局
        sql = f'delete from download where taskLine={row};'

        self.con.execute(sql)
        # self.con.commit()

    def deleteBookShelfLayoutInfo(self,
                                  bookNums: int) -> None:  # 删除书架界面布局
        sql = f'delete from bookshelf where bookNums={bookNums};'
        self.con.execute(sql)
        # self.con.commit()

    def deleteIsInBookInfoDatabase(self, serialNumber: int):
        sql = f'delete from bookinfo where chapterSerialNumber={serialNumber}'
        self.con.execute(sql)
        # self.con.commit()

    def deleteIsInBookInfoDatabase_BookShelf(self, bookNums: int):
        sql = f'delete from bookinfo where chapterSerialNumber=(select bookSerialNumber from bookshelf where bookNums={bookNums})'
        self.con.execute(sql)
        # self.con.commit()

    def cleanUpRedundantSpace(self):
        sql = 'vacuum'
        self.con.execute(sql)
        # self.con.commit()
