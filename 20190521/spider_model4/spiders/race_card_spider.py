from url.urlManager import singleton_url
from chromeDriver import singleton_chrome
import time
from lxml import etree
from db import race_card_db
from common import common


class RaceCardSpider(object):

    def setParams(self, from_date, to_date, rmLoaded):
        self.from_date = from_date
        self.to_date = to_date
        self.rmLoaded = rmLoaded

    def spider_start(self):
        future_url_list = singleton_url.GetFutureRaceCardUrlList()
        for url in future_url_list:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(0.1)
            race_card_parse = RaceCardParse(singleton_chrome.driver.page_source)
            race_card_db.exportToFutureDb(race_card_parse.race_info, race_card_parse.race_card_table)

        history_url_list = singleton_url.GetHistoryRaceCardUrlList(self.from_date, self.to_date, self.rmLoaded)
        for url in history_url_list:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(0.8)
            race_card_parse = RaceCardParse(singleton_chrome.driver.page_source)
            race_card_db.exportToHistoryDb(race_card_parse.race_info, race_card_parse.race_card_table)


class RaceCardParse(object):

    def __init__(self, page_source):
        self.race_info = {}
        self.race_card_table = []
        self.__parse_page(page_source)

    def __parse_page(self, page_source):
        html = etree.HTML(page_source)

        # race info
        table_info = html.xpath('//table[@class="font13 lineH20 tdAlignL"]')
        if len(table_info) > 0:
            race_No_text = table_info[0].xpath('.//td//span')
            array_race_No = race_No_text[0].xpath('string(.)').split('-')
            self.race_info['race_No'] = int(array_race_No[0].replace('Race', ''))

            info_lines = table_info[0].xpath('.//td//br')
            info_line_1 = info_lines[0].tail.strip()
            array_date_site_startTime = info_line_1.split(',')
            array_race_date_md = array_date_site_startTime[1].strip().split(' ')
            month = common.toMonth(array_race_date_md[0].strip())
            day = array_race_date_md[1].strip()
            year = array_date_site_startTime[2].strip()
            self.race_info['race_date'] = year + common.toDoubleDigitStr(month) + day
            self.race_info['site'] = array_date_site_startTime[3].strip()
            self.race_info['startTime'] = array_date_site_startTime[4].strip()

            info_line_2 = info_lines[1].tail.strip()
            array_split_dst = info_line_2.split('0M')
            print('array_split_dst:', array_split_dst)
            array_split_dst_0 = array_split_dst[0].split(',')
            self.race_info['course'] = ''.join(array_split_dst_0[: len(array_split_dst_0) - 1])
            array_split_dst_1 = array_split_dst[1].split(',')
            self.race_info['going'] = array_split_dst_1[len(array_split_dst_1) - 1].strip()
            array_course_dst_going = info_line_2.split(',')
            print('array_course_dst_going:', array_course_dst_going)
            for text in array_course_dst_going:
                if '0M' in text:
                    self.race_info['distance'] = int(text.replace('M', ''))
            # if len(array_course_dst_going) == 3 or len(array_course_dst_going) == 2:
            #     self.race_info['going'] = 'GOOD'
            #     self.race_info['distance'] = int(array_course_dst_going[len(array_course_dst_going) - 1].replace('M', ''))
            #     self.race_info['course'] = ''.join(array_course_dst_going[: len(array_course_dst_going) - 1])
            # else:
            #     self.race_info['going'] = array_course_dst_going[len(array_course_dst_going) - 1].strip()
            #     self.race_info['distance'] = int(array_course_dst_going[len(array_course_dst_going) - 2].replace('M', ''))
            #     self.race_info['course'] = ''.join(array_course_dst_going[: len(array_course_dst_going) - 2])

            info_line_3 = info_lines[2].tail.strip()
            array_bonus_cls = info_line_3.split(',')
            self.race_info['cls'] = array_bonus_cls[len(array_bonus_cls) - 1].strip()
            array_bonus = ''.join(array_bonus_cls[: len(array_bonus_cls) - 2]).split(':')
            self.race_info['bonus'] = int(array_bonus[1].replace('$', ''))

        # race card table
        race_card_table = html.xpath('//table[@class="draggable hiddenable"]')
        if len(race_card_table) > 0:
            trs_card = race_card_table[0].xpath('.//tr')
            for each_tr in trs_card[1:]:
                tds_row = each_tr.xpath('./td')
                row = []
                for each_td in tds_row:
                    image_block = each_td.xpath('./img/@alt')
                    if len(image_block) > 0:
                        block = image_block[0]
                    else:
                        block = each_td.xpath('string(.)').replace('\xa0', '').strip()
                    row.append(block)
                self.race_card_table.append(row)
                print('row:', row)

        print('race_info:', self.race_info)

