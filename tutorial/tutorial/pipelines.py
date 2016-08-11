# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import MySQLdb
import MySQLdb.cursors

SETTINGS = get_project_settings()
class TutorialPipeline(object):

    def process_item(self, item, spider):
        """
        :param item:
        :param spider:
        :return:
        """
        return item


class MySQLStorePipeline(object):
    """
        将数据插入数据库
    """
    def __init__(self, status):
        """
        :param status:
        :return:
        """
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host=SETTINGS["DB_HOST"],
                                            user=SETTINGS['DB_USER'],
                                            passwd=SETTINGS['DB_PASSWORD'],
                                            port=SETTINGS['DB_PORT'],
                                            db=SETTINGS['DB_DB'],
                                            charset='utf8',
                                            use_unicode=True,
                                            cursorclass=MySQLdb.cursors.DictCursor)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_item(self, item, spider):
        """
        :param item:
        :param spider:
        :return:
        """
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def spider_closed(self, spider):
        """
        :param spider:
        :return:
        """
        self.dbpool.close()

    def _insert_record(self, tx, ):
        pass
