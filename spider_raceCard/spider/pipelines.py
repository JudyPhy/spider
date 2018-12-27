# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from spider.db import raceCard
from spider.items import RaceCardItem
from spider.db.db import singleton_ScrubDb
import os


class SpiderPipeline(object):
    def process_item(self, item, spider):
        # race result
        if isinstance(item, RaceCardItem):
            raceCard.process_RaceCardItem(item)
        return item

    def close_spider(self, spider):
        singleton_ScrubDb.connect.close()
        os.remove('flag')
