from horse_parse import HorseInfoParse
from url.urlManager import singleton_url
from common import common
from db import horse as horse_db
from chromeDriver import singleton_chrome


class RaceHorseSpider(object):

    def start_requests(self):
        url_list = singleton_url.getUrlList()
        common.log('need spider url count=' + str(len(url_list)))

        for url in url_list:
            horse_parse = HorseInfoParse(url)
            self.exportToTable(horse_parse)

        singleton_chrome.quit()

    def getItem(self, season, info, horse_info):
        item_horse = {}
        item_horse['name'] = horse_info['name']
        item_horse['code'] = horse_info['code']
        item_horse['season'] = season

        item_horse['race_id'] = info['race_id']
        item_horse['pla'] = info['pla']
        item_horse['race_date'] = info['race_date']
        item_horse['rc_track_course'] = info['rc_track_course']
        item_horse['dist'] = info['dist']
        item_horse['g'] = info['g']
        item_horse['class'] = info['class']
        item_horse['dr'] = info['dr']
        item_horse['rtg'] = info['rtg']
        item_horse['trainer'] = info['trainer']
        item_horse['jockey'] = info['jockey']
        item_horse['lbw'] = info['lbw']
        item_horse['win_odds'] = info['win_odds']
        item_horse['act_wt'] = info['act_wt']
        item_horse['running_position'] = info['running_position']
        item_horse['finish_time'] = info['finish_time']
        item_horse['declar_horse_wt'] = info['declar_horse_wt']
        item_horse['gear'] = info['gear']

        return item_horse

    def exportToTable(self, horse_parse):
        seasonInfo = horse_parse.horse_seasonInfo
        for season, rows in seasonInfo.items():
            print(season, len(rows))
            for row in rows:
                item = self.getItem(season, row, horse_parse.horse_info)
                horse_db.process_HorseInfoItem(item)

