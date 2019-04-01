from common import common
from chromeDriver import singleton_chrome
import time


class PageParse(object):
    BASE_URL = 'http://hk.racing.nextmedia.com/emodds.php?date={0}&page={1}'

    def __init__(self, race_date, race_no):
        self.sectionalTime = []
        self.oddsDict = {}
        self.__start_requests(race_date, race_no)
        pass

    def __start_requests(self, race_date, race_no):
        url = self.BASE_URL.replace('{0}', race_date).replace('{1}', str(race_no))
        print('request=>', url)
        try:
            singleton_chrome.driver.get(url)
            time.sleep(0.1)
            self.__parseSectionalOddsTable()
        except Exception as error:
            common.log('parse page error:' + str(error))

    def __parseSectionalOddsTable(self):
        self.oddsDict = {}    # horse_no & []
        self.sectionalTime = []
        tables = singleton_chrome.driver.find_elements_by_xpath('//table')
        if len(tables) > 1:
            trs = tables[1].find_elements_by_xpath('.//tr')
            tds_line2 = trs[1].find_elements_by_xpath('.//td')
            for td_line2 in tds_line2[3:]:
                self.sectionalTime.append(td_line2.text)
            print(self.sectionalTime)
            for tr_line in trs[2:]:
                tds_line = tr_line.find_elements_by_xpath('.//td')
                horse_no = int(tds_line[0].text)
                if horse_no not in self.oddsDict.keys():
                    self.oddsDict[horse_no] = []
                else:
                    continue
                # horse_name = tds_line[1].text
                # self.oddsDict[horse_no].append(horse_name)
                if tds_line[2].text == '':
                    draw = 0
                else:
                    draw = int(tds_line[2].text)
                self.oddsDict[horse_no].append(draw)
                for td_line in tds_line[3:]:
                    self.oddsDict[horse_no].append(td_line.text)
                print(horse_no, self.oddsDict[horse_no])

