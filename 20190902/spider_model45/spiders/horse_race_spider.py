from url.urlManager import singleton_url
from chromeDriver import singleton_chrome
import time
from lxml import etree
from db import horse_race_db


class HorseRaceSpider(object):

    def setParams(self, from_date, to_date, rmLoaded):
        self.from_date = from_date
        self.to_date = to_date
        self.rmLoaded = rmLoaded

    def spider_start(self):
        url_list = singleton_url.GetHorseRaceUrlList(self.from_date, self.to_date, self.rmLoaded)
        for url in url_list:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(0.1)
            horse_race_parse = HorseRaceParse(singleton_chrome.driver.page_source)
            horse_race_db.exportToDb(horse_race_parse.horse_info, horse_race_parse.horse_seasonInfo)


class HorseRaceParse(object):

    def __init__(self, page_source):
        self.horse_info = {}
        self.horse_seasonInfo = {}
        self.__parse_page(page_source)

    def __parse_page(self, page_source):
        html = etree.HTML(page_source)

        # horse info
        horse_info = html.xpath('//span[@class="title_text"]')
        for info in horse_info[:1]:
            name = info.text.replace('&nbsp;', '').replace('(Retired)', '')
            if '(' in name:
                array_name = name.split('(')
                self.horse_info['name'] = array_name[0].strip()
                self.horse_info['code'] = array_name[len(array_name) - 1].replace(')', '').strip()
            else:
                self.horse_info['name'] = name.strip()
                self.horse_info['code'] = 0
            print('name:', self.horse_info['name'], ' code:', self.horse_info['code'])

        # race detail
        table_horse_race = html.xpath('//table[@class="bigborder"]')
        if len(table_horse_race) > 0:
            trs = table_horse_race[0].xpath('.//tr')
            season = ''
            for tr in trs[1:]:
                if tr.xpath('string(.)').strip() == '':
                    continue
                tds = tr.xpath('./td')
                if len(tds) == 1:
                    season = tds[0].xpath('string(.)').strip()
                    print('season:', season)
                elif len(tds) == 19 and season != '':
                    if season not in self.horse_seasonInfo.keys():
                        self.horse_seasonInfo[season] = []
                    dict = {}
                    dict['race_id'] = tds[0].xpath('string(.)').strip()
                    dict['pla'] = tds[1].xpath('string(.)').strip()
                    dict['race_date'] = tds[2].xpath('string(.)').strip()
                    dict['rc_track_course'] = tds[3].xpath('string(.)').strip()
                    dict['dist'] = tds[4].xpath('string(.)').strip()
                    dict['g'] = tds[5].xpath('string(.)').strip()
                    dict['class'] = tds[6].xpath('string(.)').strip()
                    dict['dr'] = tds[7].xpath('string(.)').strip()
                    dict['rtg'] = tds[8].xpath('string(.)').strip()
                    dict['trainer'] = tds[9].xpath('string(.)').strip()
                    dict['jockey'] = tds[10].xpath('string(.)').strip()
                    dict['lbw'] = tds[11].xpath('string(.)').strip()
                    dict['win_odds'] = tds[12].xpath('string(.)').strip()
                    dict['act_wt'] = tds[13].xpath('string(.)').strip()

                    running_position = tds[14].xpath('string(.)').strip()
                    array_rp = running_position.split(' ')
                    str_rp = ''
                    for item_rp in array_rp:
                        p = item_rp.replace(' ', '')
                        if p != '':
                            str_rp += p + '|'
                    if str_rp[len(str_rp) - 1] == '|':
                        str_rp = str_rp[: len(str_rp) - 1]
                    dict['running_position'] = str_rp

                    dict['finish_time'] = tds[15].xpath('string(.)').strip()
                    dict['declar_horse_wt'] = tds[16].xpath('string(.)').strip()
                    dict['gear'] = tds[17].xpath('string(.)').strip()
                    # print(dict)

                    self.horse_seasonInfo[season].append(dict)
                else:
                    print('table column error')

