from scrapy import cmdline
from spider.db import db


cmdline.execute("scrapy crawl raceResults".split())

