from common import common
from chromeDriver import singleton_chrome
import time


class SectionalTimeParse(object):

    def __init__(self, url):
        # race info
        self.raceInfo = {}
        self.raceInfo['race_date'] = ''
        self.raceInfo['race_No'] = 0
        self.raceInfo['site'] = ""
        self.raceInfo['cls'] = 0
        self.raceInfo['distance'] = 0
        self.raceInfo['going'] = ''
        self.raceInfo['course'] = ''
        self.sectionTimeInfo = []

        self.request(url)

    def request(self, url):
        print('request=>', url)
        try:
            singleton_chrome.driver.get(url)
            time.sleep(0.2)
            self.__parseRaceInfo()
            self.__parseSectionalTimeTable()
        except Exception as error:
            common.log('parse page error:' + str(error))

    def __parseSectionalTimeTable(self):
        table_secTime = singleton_chrome.driver.find_elements_by_xpath('//table[@class="table_bd f_tac race_table"]')
        if len(table_secTime) > 0:
            tbody = table_secTime[0].find_elements_by_xpath('./tbody')
            if len(tbody) > 0:
                trs = tbody[0].find_elements_by_xpath('./tr')
                for each_tr in trs:
                    tds = each_tr.find_elements_by_xpath('./td')
                    if len(tds) == 10:
                        row = {}
                        row['finishing_order'] = tds[0].text
                        row['horse_No'] = tds[1].text
                        array_horse = tds[2].text.split('(')
                        row['horse_name'] = array_horse[0].strip()
                        row['horse_code'] = array_horse[1].replace(')', '').strip()

                        n = 1
                        for i in range(3, 9):
                            key_sec_pos = 'sec' + str(n) + '_pos'
                            key_sec_i = 'sec' + str(n) + '_i'
                            key_time = 'sec' + str(n) + '_time'
                            row[key_sec_pos] = ''
                            row[key_sec_i] = ''
                            row[key_time] = ''

                            p_sec = tds[i].find_elements_by_xpath('./p')
                            if len(p_sec) == 2:
                                row[key_time] = p_sec[1].text
                                span_sec = p_sec[0].find_elements_by_xpath('./span')
                                if len(span_sec) > 0:
                                    row[key_sec_pos] = span_sec[0].text
                                i_sec = p_sec[0].find_elements_by_xpath('./i')
                                if len(i_sec) > 0:
                                    row[key_sec_i] = i_sec[0].text
                            else:
                                pass
                                # common.log('p_sec length error')
                            n += 1

                        row['time'] = tds[9].text.strip()
                        self.sectionTimeInfo.append(row)
                        # print(row)
                    else:
                        common.log("each_tr's td length error")
        else:
            pass

    def __parseRaceInfo(self):
        div_date = singleton_chrome.driver.find_elements_by_xpath('.//div[@class="search"]')
        if len(div_date) > 0:
            span_date = div_date[0].find_elements_by_xpath('.//span')
            if len(span_date) > 0:
                str_date = span_date[0].text
                array_date = str_date.split(',')
                if len(array_date) == 2:
                    self.raceInfo['race_date'] = array_date[0].replace('Meeting Date:', '').strip()
                    self.raceInfo['site'] = array_date[1].replace(' ', '').strip()
                else:
                    common.log('race date array parse error')
            else:
                common.log('race date span parse error')
        else:
            common.log('race date div parse error')

        div_other = singleton_chrome.driver.find_elements_by_xpath('.//div[@class="Race f_clear"]')
        if len(div_other) > 0:
            p_raceNo = div_other[0].find_elements_by_xpath('.//p')
            if len(p_raceNo) > 0:
                self.raceInfo['race_No'] = p_raceNo[0].text.replace('Race', '').strip()
            else:
                common.log('race No. p parse error')

            span_other = div_other[0].find_elements_by_xpath('.//span')
            if len(span_other) > 0:
                str_other = span_other[0].text
                flag = False
                list_str_other = list(str_other)
                for index in range(len(list_str_other)):
                    if list_str_other[index] == '(':
                        flag = True
                    elif list_str_other[index] == '-':
                        if flag:
                            list_str_other[index] = ' '
                    elif list_str_other[index] == ')':
                        flag = False
                str_other = ''.join(list_str_other)
                array_other = str_other.split('-')
                # print('array_other:', array_other)
                if len(array_other) == 6:
                    self.raceInfo['cls'] = array_other[0].strip()
                    self.raceInfo['distance'] = int(array_other[1].replace('M', ''))
                    array_course = array_other[4].strip().split('"')
                    if len(array_course) > 1:
                        self.raceInfo['course'] = array_course[1]
                    else:
                        common.log('race course array parse error')
                    self.raceInfo['going'] = array_other[5].strip()
                elif len(array_other) == 5:
                    self.raceInfo['cls'] = array_other[0].strip()
                    self.raceInfo['distance'] = int(array_other[1].replace('M', ''))
                    array_course = array_other[3].strip().split('"')
                    if len(array_course) > 1:
                        self.raceInfo['course'] = array_course[1]
                    else:
                        self.raceInfo['course'] = array_other[3].strip()
                    self.raceInfo['going'] = array_other[4].strip()
                else:
                    common.log('race other array parse error')
            else:
                common.log('race other span parse error')
        else:
            common.log('race other div parse error')
        print('race_date:', self.raceInfo['race_date'], ', race_no:', self.raceInfo['race_No'], ', cls:',
              self.raceInfo['cls'], ', site:', self.raceInfo['site'], ', distance:', self.raceInfo['distance'],
              ', course:', self.raceInfo['course'], ', going:', self.raceInfo['going'])
    pass



