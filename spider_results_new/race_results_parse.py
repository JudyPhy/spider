from chromeDriver import singleton_chrome
import time


class RaceResultsParse(object):

    def __init__(self, url):
        # race info
        self.race_date = ''
        self.race_id = 0
        self.race_No = 0
        self.site = ""
        self.cls = 0
        self.distance = 0
        self.bonus = 0
        self.going = ''
        self.course = ''

        self.table_rank_result = []
        self.table_payout = []
        self.winHorseInfo = {}

        self.__parse(url)

    def __parseRankTable(self):
        divs_rank = singleton_chrome.driver.find_elements_by_xpath('//div[@class="performance"]')
        if len(divs_rank) > 0:
            trs = divs_rank[0].find_elements_by_xpath('.//tbody//tr')
            for each_tr in trs:
                tds = each_tr.find_elements_by_xpath('./td')
                if len(tds) == 12:
                    row = []
                    for each_td in tds:
                        divs_pos = each_td.find_elements_by_xpath('./div[1]/div')
                        if len(divs_pos) > 0:
                            block = ''
                            for pos in divs_pos:
                                if pos.text == '':
                                    continue
                                block += pos.text + ','
                            row.append(block)
                        else:
                            block = each_td.text
                            row.append(block)
                    self.table_rank_result.append(row)
                elif len(tds) == 11:
                    # 没有running position
                    row = []
                    for each_td in tds:
                        block = each_td.text
                        row.append(block)
                    row.insert(9, '')
                    self.table_rank_result.append(row)
        else:
            pass
        for row in self.table_rank_result:
            print(row)

    def __parseRaceInfo(self):
        divs_meeting = singleton_chrome.driver.find_elements_by_xpath('//div[@class="raceMeeting_select"]')
        if len(divs_meeting) > 0:
            date_site = divs_meeting[0].find_element_by_xpath('.//span[1]').text
            array_date_site = date_site.split('   ')
            if len(array_date_site) == 2:
                self.race_date = array_date_site[0].split(':')[1].strip()
                self.site = array_date_site[1].replace(' ', '')
            else:
                pass
        else:
            pass

        divs_info = singleton_chrome.driver.find_elements_by_xpath('//div[@class="race_tab"]')
        if len(divs_info) > 0:
            thead = divs_info[0].find_element_by_xpath('.//thead/tr[1]/td[1]')
            if ('(' in thead.text) and (')' in thead.text):
                self.race_id = thead.text.split('(')[1].split(')')[0]
                self.race_No = thead.text.split('(')[0].replace(' ', '').replace('RACE', '')
            else:
                pass

            tbody = divs_info[0].find_element_by_xpath('.//tbody')
            text_cls_dis = tbody.find_element_by_xpath('./tr[2]/td[1]').text
            if '-' in text_cls_dis:
                temp_array = text_cls_dis.split('-')
                self.cls = temp_array[0].replace(' ', '')
                self.distance = temp_array[1].replace('M', '').strip()
            else:
                pass

            self.going = tbody.find_element_by_xpath('./tr[2]/td[3]').text

            text_bonus = tbody.find_element_by_xpath('./tr[4]/td[1]').text
            self.bonus = text_bonus.replace(',', '').replace('HK$', '').replace(' ', '')

            text_course = tbody.find_element_by_xpath('./tr[3]/td[3]').text
            self.course = text_course.replace('&quot;', '')
        else:
            pass

        print('race_date:', self.race_date, ' site:', self.site, ' race_id:', self.race_id,' race_No:', self.race_No,
              ' cls:', self.cls, '  distance:', self.distance, ' bonus:', self.bonus, ' course:', self.course,
              ' going:', self.going)
        pass

    def __parsePayout(self,response):
        table = response.xpath('.//table[@class="tableBorder trBgBlue tdAlignC font13 fontStyle"]')
        if len(table)>0:
            trs = table[0].xpath('./tr')[2:]
            cur_pool = ''
            for tr in trs:
                row = {}
                tds = tr.xpath('./td')
                if len(tds) == 3:
                    cur_pool = tds[0].xpath('string(.)').extract()[0]
                    row['pool'] = cur_pool
                    row['winning_combination'] = []
                    row['winning_combination'].append(tds[1].xpath('string(.)').extract()[0])
                    row['dividend'] = []
                    row['dividend'].append(tds[2].xpath('string(.)').extract()[0])
                    self.table_payout.append(row)

                elif len(tds) == 2:
                    find = False
                    for pool in self.table_payout:
                        if pool['pool'] == cur_pool:
                            find = True
                            pool['winning_combination'].append(tds[0].xpath('string(.)').extract()[0])
                            pool['dividend'].append(tds[1].xpath('string(.)').extract()[0])
                    if not find:
                        row['pool'] = cur_pool
                        row['winning_combination'] = []
                        row['winning_combination'].append(tds[0].xpath('string(.)').extract()[0])
                        row['dividend'] = []
                        row['dividend'].append(tds[1].xpath('string(.)').extract()[0])
                        self.table_payout.append(row)
        else:
            pass

    def __parseWinHorseInfo(self,response):
        table = response.xpath('.//table[@class="trBgGrey3"]')
        if len(table)>0:
            trs = table[0].xpath('./tr')
            if len(trs)>2:
                tds = trs[2].xpath('./td')
                if len(tds)>1:
                    self.winHorseInfo['win_horse_name'] = tds[0].xpath('string(.)').extract()[0].replace(' ','')
                    str_info = tds[1].xpath('string(.)').extract()[0].replace(' ','')
                    strs = str_info.split('\r\n')
                    self.winHorseInfo['sire'] = strs[2].split(':')[1]
                    self.winHorseInfo['dam'] = strs[4].split(':')[1]
                else:
                    pass
            else:
                pass
        else:
            pass

    def __parse(self,url):
        try:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(0.1)
            self.__parseRaceInfo()
            self.__parseRankTable()
            # self.__parsePayout(url)
            # self.__parseWinHorseInfo(url)
        finally:
            pass

