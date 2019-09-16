from url.urlManager import singleton_url
from chromeDriver import singleton_chrome
import time
from lxml import etree
from db import race_results_db


class RaceResultsSpider(object):

    def setParams(self, from_date, to_date, rmLoaded):
        self.from_date = from_date
        self.to_date = to_date
        self.rmLoaded = rmLoaded

    def spider_start(self):
        url_list = singleton_url.GetRaceResultsUrlList(self.from_date, self.to_date, self.rmLoaded)
        for url in url_list:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(0.1)
            race_results_parse = RaceResultsParse(singleton_chrome.driver.page_source)
            race_results_db.exportToDb(race_results_parse.race_info, race_results_parse.rank_table)


class RaceResultsParse(object):

    def __init__(self, page_source):
        self.race_info = {}
        self.rank_table = []
        self.__parse_page(page_source)

    def __parse_page(self, page_source):
        html = etree.HTML(page_source)

        # race info
        date_site_part = html.xpath('//div[@class="raceMeeting_select"][1]//span[1]')
        if len(date_site_part) > 0:
            date_site_text = date_site_part[0].xpath('string(.)')
            array_date_site_text = date_site_text.split(':')
            if len(array_date_site_text) == 2:
                array_date_site = array_date_site_text[1].strip().split(' ')
                array_date = array_date_site[0].strip().split('/')
                self.race_info['race_date'] = (array_date[2] + array_date[1] + array_date[0]).replace(' ', '')
                self.race_info['site'] = ''
                for str in array_date_site[1:]:
                    self.race_info['site'] += str

        thead = html.xpath('//div[@class="race_tab"][1]//thead/tr[1]/td[1]')
        if len(thead) > 0:
            info_text = thead[0].xpath('string(.)')
            if ('(' in info_text) and (')' in info_text):
                self.race_info['race_id'] = info_text.split('(')[1].split(')')[0]
                self.race_info['race_No'] = info_text.split('(')[0].replace(' ', '').replace('RACE', '')

        cls_dis_info = html.xpath('//div[@class="race_tab"][1]//tbody[1]/tr[2]/td[1]')
        if len(cls_dis_info) > 0:
            cls_dis_text = cls_dis_info[0].xpath('string(.)')
            if '-' in cls_dis_text:
                temp_array = cls_dis_text.split('-')
                self.race_info['cls'] = temp_array[0].replace(' ', '')
                self.race_info['distance'] = temp_array[1].replace('M', '').strip()

        going_info = html.xpath('//div[@class="race_tab"][1]//tbody[1]/tr[2]/td[3]')
        if len(going_info) > 0:
            self.race_info['going'] = going_info[0].xpath('string(.)')

        bonus_info = html.xpath('//div[@class="race_tab"][1]//tbody[1]/tr[4]/td[1]')
        if len(bonus_info) > 0:
            text_bonus = bonus_info[0].xpath('string(.)')
            self.race_info['bonus'] = text_bonus.replace(',', '').replace('HK$', '').replace(' ', '')

        course_info = html.xpath('//div[@class="race_tab"][1]//tbody[1]/tr[3]/td[3]')
        if len(bonus_info) > 0:
            text_course = course_info[0].xpath('string(.)')
            self.race_info['course'] = text_course.replace('&quot;', '')
        print('race_info:', self.race_info)

        # rank table
        rank_trs = html.xpath('//div[@class="performance"][1]//tbody//tr')
        for each_tr in rank_trs:
            tds = each_tr.xpath('./td')
            if len(tds) == 12:
                row = []
                for each_td in tds:
                    divs_pos = each_td.xpath('./div[1]/div')
                    if len(divs_pos) > 0:
                        block = ''
                        for pos in divs_pos:
                            pos_text = pos.xpath('string(.)').strip()
                            if pos_text == '':
                                continue
                            block += pos_text + ','
                        row.append(block)
                    else:
                        block = each_td.xpath('string(.)').strip()
                        row.append(block)
                if '-' in row[len(row) - 1]:
                    row[len(row) - 1] = '-1'
                self.rank_table.append(row)
            elif len(tds) == 11:
                # 没有running position
                row = []
                for each_td in tds:
                    block = each_td.xpath('string(.)').strip()
                    row.append(block)
                row.insert(9, '')
                if '-' in row[len(row) - 1]:
                    row[len(row) - 1] = '-1'
                self.rank_table.append(row)

        for row in self.rank_table:
            array_horse_name_code = row[2].split('(')
            if len(array_horse_name_code) == 2:
                row[2] = array_horse_name_code[0]
                row.insert(3, array_horse_name_code[1].replace(')', ''))
            else:
                row.insert(3, '')
            print(row)

