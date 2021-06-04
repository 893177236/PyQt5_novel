# encoding=utf-8
###
# @Description:日志封装文件
# @Author:fatih
# @Date:2020-12-3010:48:00
# @FilePath:\mechineInfo\utils\log.py
# @LastEditors:fatih
# @LastEditTime:2021-01-1116:18:30
###
import logging
from colorama import Fore, Style
from termcolor import colored


# 既把日志输出到控制台，还要写入日志文件
class Logger(object):
    """
    指定保存日志的文件路径，日志级别，以及调用文件
    将日志存入到指定的文件中
    """
    def __init__(self, loglevel=1, loggername=None):
        if loglevel == 1:
            loglevel = logging.INFO
        elif loglevel == 2:
            loglevel = logging.DEBUG
        elif loglevel == 3:
            loglevel = logging.WARNING
        elif loglevel == 4:
            loglevel = logging.ERROR
        else:
            loglevel = logging.CRITICAL
        # 创建一个logger
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(loglevel)

        # 创建一个handler，用于写入日志文件
        # fh = logging.FileHandler(logname)
        # fh.setLevel(loglevel)
        if not self.logger.handlers:
            # 再创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(loglevel)
            # 定义handler的输出格式
            # formatter=logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
            formatter = logging.Formatter(
                '[%(levelname)s] %(asctime)s - %(filename)s - %(funcName)s - [line:%(lineno)d]:%(message)s')
            # fh.setFormatter(formatter)

            formatter = _ColorfulFormatter(
                colored('[%(levelname)s] %(asctime)s - %(filename)s - %(funcName)s - [line:%(lineno)d]:%(message)s')
                , datefmt="%Y/%m/%d %H:%M:%S",
                root_name="debug")
            ch.setFormatter(formatter)
            # 给logger添加handler
            # self.logger.addHandler(fh)
            self.logger.addHandler(ch)

            # self.logger.fatal("addhandler")
            # self.logger.fatal("setlogger")

    def getlog(self):
        # self.logger.fatal("getlogger")
        return self.logger

    def debug(self, msg):
        """
        定义输出的颜色debug--white，info--green，warning/error/critical--red
        :param msg: 输出的log文字
        :return:
        """
        self.logger.debug(Fore.WHITE + str(msg) + Style.RESET_ALL)

    def info(self, msg):
        self.logger.info(Fore.GREEN + str(msg) + Style.RESET_ALL)

    def warning(self, msg):
        self.logger.warning(Fore.RED + str(msg) + Style.RESET_ALL)

    def error(self, msg):
        self.logger.error(Fore.RED + str(msg) + Style.RESET_ALL)


class _ColorfulFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self._root_name = kwargs.pop("root_name") + "."
        self._abbrev_name = kwargs.pop("abbrev_name", "")
        if len(self._abbrev_name):
            self._abbrev_name = self._abbrev_name + "."
        super(_ColorfulFormatter, self).__init__(*args, **kwargs)

    def formatMessage(self, record):
        record.name = record.name.replace(self._root_name, self._abbrev_name)
        log = super(_ColorfulFormatter, self).formatMessage(record)
        if record.levelno == logging.WARNING:
            levelname_color = ""
            levelname_on_color = "on_red"
            other_color = "cyan"
            text_color = "red"
            text_on_color = ""
            attrs = ["dark"]
        elif record.levelno == logging.ERROR or record.levelno == logging.CRITICAL:
            levelname_color = ""
            levelname_on_color = "on_red"
            other_color = "cyan"
            text_color = "red"
            text_on_color = "on_grey"
            attrs = ["blink", "underline"]

        elif record.levelno == logging.INFO:
            levelname_color = "grey"
            levelname_on_color = "on_white"
            other_color = "cyan"
            text_color = "yellow"
            text_on_color = ""
            attrs = ["blink"]
        else:
            return log
        if levelname_color:
            levelname = colored(text=f"[{record.levelname}] ", color=levelname_color, on_color=levelname_on_color,
                                attrs=attrs)
        else:
            levelname = colored(text=f"[{record.levelname}] ", on_color=levelname_on_color, attrs=attrs)
        othermsg = colored(text=f"{record.asctime} - {record.filename} - {record.funcName} - ", color=other_color,
                           attrs=attrs)
        line = colored(text=f"[line:{record.lineno}]:", color="red", attrs=attrs)
        if text_on_color:
            msg = colored(text=f"{record.message}", color=text_color, on_color=text_on_color, attrs=attrs)
        else:
            msg = colored(text=f"{record.message}", color=text_color, attrs=attrs)
        # return prefix + " " + log
        return levelname + othermsg + line + msg
