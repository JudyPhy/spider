from url.urlManager import singleton_url
from chromeDriver import singleton_chrome
import time
from lxml import etree
from db import display_sectional_time_db


class DisplaySectionalTimeSpider(object):

    def setParams(self, from_date, to_date, rmLoaded):
        self.from_date = from_date
        self.to_date = to_date
        self.rmLoaded = rmLoaded

    def spider_start(self):
        url_list = singleton_url.GetDisplaySectionalTimeUrlList(self.from_date, self.to_date, self.rmLoaded)
        for url in url_list:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(0.1)
            display_sectional_time_parse = DisplaySectionalTimeParse(singleton_chrome.driver.page_source)
            display_sectional_time_db.exportToDb(display_sectional_time_parse.race_info, display_sectional_time_parse.sectional_time_table)


class DisplaySectionalTimeParse(object):

    def __init__(self, page_source):
        self.race_info = {}
        self.sectional_time_table = []
        self.__parse_page(page_source)

    def __parse_page(self, page_source):
        html = etree.HTML(page_source)

        # race info
        date_site_ele = html.xpath('.//div[@class="search"][1]//span[1]')
        if len(date_site_ele) > 0:
            date_site_text = date_site_ele[0].xpath('string(.)')
            array_date_site = date_site_text.split(',')
            array_date = array_date_site[0].replace('Meeting Date:', '').strip().split('/')
            self.race_info['race_date'] = array_date[2] + array_date[1] + array_date[0]
            self.race_info['site'] = array_date_site[1].replace(' ', '').strip()

        race_No_ele = html.xpath('.//div[@class="Race f_clear"][1]//p')
        if len(race_No_ele) > 0:
            self.race_info['race_No'] = int(race_No_ele[0].xpath('string(.)').replace('Race', ''))

        cls_dst_course_going_ele = html.xpath('.//div[@class="Race f_clear"][1]//span[1]')
        if len(cls_dst_course_going_ele) > 0:
            cls_dst_course_going_text = cls_dst_course_going_ele[0].xpath('string(.)')
            # check split flag
            flag = False
            cls_dst_course_going_text_list = list(cls_dst_course_going_text)
            for index in range(len(cls_dst_course_going_text_list)):
                if cls_dst_course_going_text_list[index] == '(':
                    flag = True
                elif (cls_dst_course_going_text_list[index] == '-') or (cls_dst_course_going_text_list[index] == '+'):
                    if flag:
                        cls_dst_course_going_text_list[index] = '|'
                elif cls_dst_course_going_text_list[index] == ')':
                    flag = False
            new_cls_dst_course_going_text = ''.join(cls_dst_course_going_text_list)
            if '|' in new_cls_dst_course_going_text:
                # split flag
                array_split = new_cls_dst_course_going_text.split('|')
                array_cls_dst = array_split[0].split('-')
                self.race_info['cls'] = array_cls_dst[0].strip()
                self.race_info['distance'] = int(array_cls_dst[1].replace('M', ''))
                array_course_going = array_split[1].split(')')[1].split('-')
                self.race_info['course'] = ''.join(array_course_going[:len(array_course_going) - 1])
                self.race_info['course'] = self.race_info['course'].strip()
                self.race_info['going'] = array_course_going[len(array_course_going) - 1].strip()
            else:
                array_split = new_cls_dst_course_going_text.split('-')
                self.race_info['cls'] = array_split[0].strip()
                self.race_info['distance'] = int(array_split[1].replace('M', ''))
                self.race_info['course'] = ''.join(array_split[2:len(array_split) - 1])
                self.race_info['course'] = self.race_info['course'].strip()
                self.race_info['going'] = array_split[len(array_split) - 1].strip()

        # sectional time table
        sectional_time_table = html.xpath('//table[@class="table_bd f_tac race_table"][1]//tbody[1]/tr')
        for each_tr in sectional_time_table:
            tds = each_tr.xpath('./td')
            if len(tds) == 10:
                row = {}
                row['finishing_order'] = tds[0].xpath('string(.)')
                row['horse_No'] = int(tds[1].xpath('string(.)'))
                array_horse = tds[2].xpath('string(.)').split('(')
                row['horse_name'] = array_horse[0].strip()
                row['horse_code'] = array_horse[1].replace(')', '').strip()

                n = 1
                for i in range(3, 9):
                    key_sec_pos = 'sec' + str(n) + '_pos'
                    key_sec_i = 'sec' + str(n) + '_i'
                    key_time = 'sec' + str(n) + '_time'
                    n += 1
                    row[key_sec_pos] = ''
                    row[key_sec_i] = ''
                    row[key_time] = ''

                    span_sec = tds[i].xpath('./p[1]/span')
                    if len(span_sec) > 0:
                        row[key_sec_pos] = span_sec[0].xpath('string(.)')
                    i_sec = tds[i].xpath('./p[1]//i')
                    if len(i_sec) > 0:
                        row[key_sec_i] = i_sec[0].xpath('string(.)')
                    p_sec = tds[i].xpath('./p')
                    if len(p_sec) > 1:
                        row[key_time] = p_sec[1].xpath('string(.)')

                row['time'] = tds[9].text.strip()
                self.sectional_time_table.append(row)
                # print(row)

        print('race_info:', self.race_info)

