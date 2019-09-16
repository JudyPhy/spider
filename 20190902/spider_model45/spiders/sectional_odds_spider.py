from url.urlManager import singleton_url
from chromeDriver import singleton_chrome
import time
from lxml import etree
from db import sectional_odds_db


class SectionalOddsSpider(object):

    def setParams(self, from_date, to_date, rmLoaded):
        self.from_date = from_date
        self.to_date = to_date
        self.rmLoaded = rmLoaded

    def spider_start(self):
        url_list = singleton_url.GetSectionalOddsUrlList(self.from_date, self.to_date, self.rmLoaded)
        for url in url_list:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(0.1)
            race_date = url.split('?date=')[1][:8]
            sectional_odds_parse = SectionalOddsParse(singleton_chrome.driver.page_source)
            sectional_odds_db.exportToDb(race_date, sectional_odds_parse.race_No, sectional_odds_parse.sectionalTime, sectional_odds_parse.oddsDict)


class SectionalOddsParse(object):

    def __init__(self, page_source):
        self.race_No = 0
        self.oddsDict = {}  # horse_no & []
        self.sectionalTime = []
        self.__parse_page(page_source)

    def __parse_page(self, page_source):
        html = etree.HTML(page_source)

        win_odds_table = html.xpath('//table[@class="small"]')
        if len(win_odds_table) > 0:
            win_odds_trs = win_odds_table[0].xpath('.//tr')
            win_odds_race_No_text = win_odds_trs[0].xpath('string(.)').strip()
            array_win_odds_race_No = win_odds_race_No_text.split(' ')
            win_odds_race_No_text = array_win_odds_race_No[0]
            self.race_No = int(win_odds_race_No_text[1: len(win_odds_race_No_text) - 1])
            win_odds_times_tds = win_odds_trs[1].xpath('./td')
            for win_odds_times_td in win_odds_times_tds[3:]:
                block = win_odds_times_td.xpath('string()').strip()
                self.sectionalTime.append(block)
            for win_odds_tr in win_odds_trs[2:]:
                win_odds_tds = win_odds_tr.xpath('./td')
                horse_No = int(win_odds_tds[0].xpath('string()'))
                horse_name = win_odds_tds[1].xpath('string()')
                draw = win_odds_tds[2].xpath('string()').strip()
                if draw == '':
                    draw = 0
                else:
                    draw = int(draw)
                cur_horse_win_odds_list = [horse_name, draw]
                for win_odds_td in win_odds_tds[3:]:
                    block = win_odds_td.xpath('string()').strip()
                    cur_horse_win_odds_list.append(block)
                self.oddsDict[horse_No] = cur_horse_win_odds_list

        # log
        print('race_No:', self.race_No, ' sectionalTime:', self.sectionalTime)
        for horse_No, array in self.oddsDict.items():
            print('horse_No=', horse_No, array)

