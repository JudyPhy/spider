from horse_parse import HorseInfoParse
from url.urlManager import singleton_url
from common import common
from db import horse as horse_db
from chromeDriver import singleton_chrome


class HorsePedigreeSpider(object):

    def start_requests(self):
        url_list = singleton_url.getUrlList()
        common.log('need spider url count=' + str(len(url_list)))

        for url in url_list:
            horse_parse = HorseInfoParse(url)
            self.exportToTable(horse_parse)

        singleton_chrome.quit()

    def getItem(self, info):
        item_horse = {}
        item_horse['name'] = info['name'].strip()
        item_horse['code'] = info['code'].strip()
        item_horse['grow'] = info['grow']
        item_horse['distance'] = info['distance']
        item_horse['track_affinity'] = info['track_affinity']
        return item_horse

    def exportToTable(self, horse_parse):
        item = self.getItem(horse_parse.horse_info)
        if item['code'] != '':
            horse_db.process_HorseInfoItem(item)

