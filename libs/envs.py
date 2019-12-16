import os
import time

from peewee import Proxy, PostgresqlDatabase, MySQLDatabase
import json
import logging
from logging import handlers

from playhouse.pool import PooledPostgresqlExtDatabase

from libs.configs import ELC_DB_CONFIG


class ELCLogger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射
    fmt = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'

    def __init__(self, file_name=None, level='debug', when='W0', back_count=4, fmt=None):
        if fmt is None:
            fmt = self.fmt
        self.logger = logging.getLogger(file_name)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        stream_handler = logging.StreamHandler()  # 往屏幕上输出
        stream_handler.setFormatter(format_str)  # 设置屏幕上显示的格式
        time_handler = handlers.TimedRotatingFileHandler(
            filename=file_name, when=when, backupCount=back_count, encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        time_handler.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(stream_handler)  # 把对象加到logger里
        self.logger.addHandler(time_handler)


os.makedirs("../logs/", exist_ok=True)
ELC_LOGGER = ELCLogger('../logs/server.log')

DATABASE_APP_PROXY = Proxy()


def setup_database_app():
    while True:
        try:
            DATABASE_APP_PROXY.initialize(
                PooledPostgresqlExtDatabase(**ELC_DB_CONFIG))
            return
        except Exception as e:
            ELC_LOGGER.logger.info("APP database not ready.... retrying in 10s: {}".format(e))
            time.sleep(10)


def setup_app():
    setup_database_app()
