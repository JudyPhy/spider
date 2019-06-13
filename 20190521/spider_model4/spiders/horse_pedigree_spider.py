from url.urlManager import singleton_url
from chromeDriver import singleton_chrome
import time
from lxml import etree
from db import horse_pedigree_db


class HorsePedigreeSpider(object):

    def setParams(self, from_date, to_date, rmLoaded):
        self.from_date = from_date
        self.to_date = to_date
        self.rmLoaded = rmLoaded

    def spider_start(self):
        url_list = singleton_url.GetHorsePedigreeUrlList(self.from_date, self.to_date, self.rmLoaded)
        for url in url_list:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(0.1)
            horse_pedigree_parse = HorsePedigreeParse(singleton_chrome.driver.page_source)
            horse_pedigree_db.exportToDb(horse_pedigree_parse.horse_info)


class HorsePedigreeParse(object):

    def __init__(self, page_source):
        self.horse_info = {}
        self.__parse_page(page_source)

    def __parse_page(self, page_source):
        html = etree.HTML(page_source)

        # horse info
        ele_name = html.xpath('//td[@class="table_title"][1]')
        if len(ele_name) > 0:
            name = ele_name[0].xpath('string(.)')
            if '(' in name:
                array_name = name.strip().split('(')
                self.horse_info['name'] = array_name[0]
                self.horse_info['code'] = array_name[len(array_name) - 1].replace(')', '').strip()
            else:
                self.horse_info['name'] = name
                self.horse_info['code'] = 0

        # horse blood
        divs_blood = html.xpath('//div[@class="newhorse-txt"]')
        if len(divs_blood) > 2:
            div = divs_blood[2].xpath('text()')
            for item in div:
                self.horse_info['grow'] = ''
                self.horse_info['track_affinity'] = ''
                if ('GROWTH' in item) and (':' in item):
                    self.horse_info['grow'] = item.split(':')[1].strip()
                elif 'DISTANCE' in item:
                    self.horse_info['distance'] = item.split(':')[1].strip()
                elif 'TRACK AFFINITY' in item:
                    self.horse_info['track_affinity'] = item.split(':')[1].strip().replace('，', ',')

        print(self.horse_info)

