from url.urlManager import singleton_url
from chromeDriver import singleton_chrome
import time
from lxml import etree
from db import course_standard_times_db


class CourseStandardTimesSpider(object):

    def setParams(self, from_date, to_date, rmLoaded):
        self.from_date = from_date
        self.to_date = to_date
        self.rmLoaded = rmLoaded

    def spider_start(self):
        url_list = singleton_url.GetCourseStandardTimesUrlList()
        for url in url_list:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(0.1)
            course_standard_times_parse = CourseStandardTimesParse(singleton_chrome.driver.page_source)
            course_standard_times_db.exportToDb(course_standard_times_parse.course_standard_times_table_rows)


class CourseStandardTimesParse(object):

    def __init__(self, page_source):
        self.course_standard_times_table_rows = []
        self.__parse_page(page_source)

    def __parse_page(self, page_source):
        html = etree.HTML(page_source)

        # course standard times table
        course_standard_times_trs = html.xpath('//table[@class="legacyTable b1px tbWidth100per bclrCCCCCC"][1]//tbody[1]/tr')
        track = ''
        for each_tr in course_standard_times_trs[2:]:
            tds = each_tr.xpath('./td')
            row = []
            for td in tds:
                p_label = td.xpath('./p')
                if len(p_label) > 0:
                    track = ''
                    for p in p_label:
                        track += p.xpath('string(.)').replace(' ', '').replace('\xa0', '').replace('\n', '')
                else:
                    block = td.xpath('string(.)')
                    row.append(block)
            row.insert(0, track)
            self.course_standard_times_table_rows.append(row)

        for row in self.course_standard_times_table_rows:
            print(row)

