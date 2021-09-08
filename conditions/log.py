# -*- coding: utf-8 -*

import logging
from logging import handlers

class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename, level, fmt='%(asctime)s - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
        if not self.logger.handlers:
            # 往屏幕上输出
            sh = logging.StreamHandler()
            # 设置屏幕上显示的格式
            sh.setFormatter(format_str)
            # 往文件里写入#指定间隔时间自动生成文件的处理器
            # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
            # S 秒
            # M 分
            # H 小时、
            # D 天、
            # W 每星期（interval=0时代表星期一）
            # midnight 每天凌晨
            th = handlers.TimedRotatingFileHandler(filename=filename, when="D", interval=1, backupCount=0)
            # 设置文件里写入的格式
            th.setFormatter(format_str)
            # 把对象加到logger里
            self.logger.addHandler(sh)
            self.logger.addHandler(th)



if __name__ == '__main__':
    log = Logger('test.log', level='info')
    content = 'test'
    log.logger.info(content)
    log.logger
