import requests
from time import sleep as time_sleep
from lxml import etree

from mock_useragent import UserAgent
from regular import Json
from log import Logger
log = Logger().getlog()

class Content:

    def __init__(self, priority: int, chapterUrl: str, chapterName: str, whichRule: int):  # 需要传入章节的url,和第几个规则
        self.priority = priority  # 优先队列，用于取出
        self.chapterUrl = chapterUrl
        self.chapterName = chapterName.strip()
        self.whichRule = whichRule
        self.now_rule = self.getUserRule()  # 当前规则
        self.content_rule = self.now_rule["content"]  # 当前规则的内容规则
        self.charset = self.now_rule["charset"]
        self.headers = {
            "User-Agent": UserAgent().random_chrome,
        }
        self.getContent()

    def __lt__(self, other):
        return self.priority < other.priority

    def getContent(self) -> dict:  # 请求网页内容，返回dict
        timeout_requests_number = 1
        frequent_requests_number = 1
        log.info("开始获取")
        while True:
            log.info("获取内容")
            if (timeout_requests_number <= 3) or (frequent_requests_number <=3):
                try:
                    resp = requests.get(url=self.chapterUrl, headers=self.headers, timeout=10,verify=False).content.decode(
                        self.charset,'ignore')
                    parseResult = self.parseResult(resp)
                    self.chapterContent = parseResult[0]
                    self.chapterContentHTML = parseResult[1]
                    break
                except requests.exceptions.Timeout:
                    log.warning(f"超时{timeout_requests_number}次，2s后重新请求")
                    time_sleep(2)
                except AttributeError:
                    log.warning(f"请求频繁{frequent_requests_number}次,3秒后重新请求")
                    time_sleep(3)
            else:
                self.chapterContent = ""
                log.error(f"已超时3次或请求频繁3次，记录该url:{self.chapterUrl}")
                break
            timeout_requests_number += 1
            frequent_requests_number+=1

    def parseResult(self, resp: str) -> str:  # xpath解析内容,返回str
        contentXpath = self.content_rule["text"]
        html = etree.HTML(resp)
        content_text_list = html.xpath(contentXpath)
        content_text = ""
        content_text_html = ""
        for content in content_text_list:
            content_text += content
            content_text_html += "<p>"+content+"</p>"
        return content_text.strip(),content_text_html
    def getUserRule(self) -> list:
        return Json().getData()[self.whichRule]
