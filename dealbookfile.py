# -*- coding: utf-8 -*-
import os

class DealBookFile:

    def __init__(self, filePath: str):
        self.initProperty(filePath=filePath)


    def dealBook(self):
        print("开始处理")
        with open(file=self.getBookPath(),mode="r+",encoding="utf8") as f:
            # allChapterSplit   = f.read().split("\n\n\n\n\n\n\n")


            # print(allChapterSplit)
            # print(f"分组出{len(allChapterSplit)}个章节")
            # print(f.readline())
            # print(f.readline())
            # print(f.readline())
            # print(f.readline())
            # print(f.readline())
            a = f.read().split(r"\u200b\u200b")
            print(a[3])
            print(len(a))
            # print(allChapterSplit)
            # for chapterList in allChapterSplit:
            #     chapterSplit = chapterList.split("\n\n\n\n")
            #     chapterName = chapterSplit[0]
            #     # chapterContent = chapterSplit[1]
            #     print(chapterName)


    def initProperty(self, filePath: str):
        self.setBookPath(filePath)

    def setBookPath(self, bookPath: str):
        if os.path.isfile(bookPath):
            self.__bookPath = bookPath
        else:
            raise Exception("空本地书籍路径")

    def getBookPath(self) -> str:
        return self.__bookPath
a = DealBookFile(filePath="D:\PythonProject\毕业设计\Download\苍穹榜：圣灵纪.txt")
a.dealBook()