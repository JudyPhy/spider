from common import common
from chromeDriver import singleton_chrome
import time
from config.myconfig import singleton as singleton_cfg


class WPSpider(object):
    # BASE_URL = 'https://bet.hkjc.com/default.aspx?url=/racing/pages/odds_wp.aspx&lang=ch&dv=local'
    # BASE_URL = 'https://bet.hkjc.com/racing/pages/odds_wp.aspx?lang=en&date=2019-01-16&venue=hv&raceno='
    BASE_URL = 'https://bet.hkjc.com/racing/pages/odds_wp.aspx?lang=en&date={0}-{1}-{2}&venue=hv&raceno={3}'

    def __init__(self, race_date, race_no):
        self.infoDict = {}
        self.wpTable = {}
        self.__start_requests(race_date, race_no)
        pass

    def __start_requests(self, race_date, race_no):
        url = self.BASE_URL.replace('{0}', race_date[: len(race_date) - 4]).\
            replace('{1}', race_date[len(race_date) - 4: len(race_date) - 2]).\
            replace('{2}', race_date[len(race_date) - 2:]).replace('{3}', str(race_no))
        print('request=>', url)
        try:
            singleton_chrome.driver.get(url)
            time.sleep(0.1)
            self.__parseRaceInfo()
            self.__parseWPTable(race_date, race_no)
        except Exception as error:
            common.log('parse page error:' + str(error))

    def __parseRaceInfo(self):
        print('__parseRaceInfo')
        self.infoDict['race_no'] = 0
        self.infoDict['race_date'] = ''
        self.infoDict['race_time'] = '00:00'
        self.infoDict['cls'] = 0
        self.infoDict['course'] = ''
        self.infoDict['distance'] = 0
        self.infoDict['going'] = ''
        tables = singleton_chrome.driver.find_elements_by_xpath('//table')
        if len(tables) > 8:
            tds = tables[8].find_elements_by_xpath('./tbody/tr/td')
            if len(tds) > 2:
                self.infoDict['race_no'] = int(tds[0].text.replace('Race', ''))
                raceInfo_text = tds[2].text
                array_raceInfo = raceInfo_text.split(',')
                if len(array_raceInfo) >= 7:
                    race_date_text = array_raceInfo[1].split('/')
                    if len(race_date_text) == 3:
                        self.infoDict['race_date'] = race_date_text[2].strip() + common.toDoubleDigitStr(race_date_text[1].strip()) + common.toDoubleDigitStr(race_date_text[0].strip())

                    self.infoDict['race_time'] = array_raceInfo[2].strip()
                    self.infoDict['cls'] = array_raceInfo[3].replace('Class', '').replace(' ', '').strip()

                    if len(array_raceInfo) == 8:
                        array_course = array_raceInfo[5].split('"')
                        if len(array_course) > 1:
                            self.infoDict['course'] = array_course[1]
                        else:
                            self.infoDict['course'] = array_raceInfo[5]

                        self.infoDict['distance'] = int(array_raceInfo[6].replace('m', ''))
                        self.infoDict['going'] = array_raceInfo[7].replace(' ', '').upper()
                        if self.infoDict['going'] == '':
                            self.infoDict['going'] = 'GOOD'
                    else:
                        array_course = array_raceInfo[4].split('"')
                        if len(array_course) > 1:
                            self.infoDict['course'] = array_course[1].strip()
                        else:
                            self.infoDict['course'] = array_raceInfo[4].strip()

                        self.infoDict['distance'] = int(array_raceInfo[5].replace('m', ''))
                        self.infoDict['going'] = array_raceInfo[6].replace(' ', '').strip().upper()
                        if self.infoDict['going'] == '':
                            self.infoDict['going'] = 'GOOD'
        pass

    def __parseWPTable(self, race_date, race_no):
        print('__parseWPTable')
        self.wpTable = {}    # horse_no & {key=>horse_name, draw, wt, jockey, trainer}
        divs = singleton_chrome.driver.find_elements_by_xpath('//div[@id="detailWPTable"]')
        if len(divs) > 0:
            tables = divs[0].find_elements_by_xpath('.//table')
            if len(tables) > 0:
                trs = tables[0].find_elements_by_xpath('./tbody/tr')
                if len(trs) > 0:
                    n = 0
                    for tr in trs[1:]:
                        tds = tr.find_elements_by_xpath('./td')
                        if len(tds) > 0:
                            if tds[0].text == 'F':
                                continue
                            horse_no = int(tds[0].text)
                            if len(tds) == 10:
                                if horse_no not in self.wpTable.keys():
                                    info = {}
                                    info['exit_race'] = False
                                    info['horse_code'] = tds[1].find_element_by_xpath('.//img').get_attribute('title').strip()
                                    info['horse_name'] = tds[2].text
                                    info['draw'] = int(tds[3].text)
                                    info['wt'] = int(tds[4].text)
                                    info['jockey'] = tds[5].text.strip()
                                    info['trainer'] = tds[6].text.strip()
                                    info['win_odds'] = tds[7].text
                                    info['pla_odds'] = tds[8].text
                                    info['win_pla'] = tds[9].text
                                    if (info['win_odds'] == 'SCR') and (info['pla_odds'] == 'SCR'):
                                        info['exit_race'] = True
                                        common.log(str(race_date) + str(race_no) + 'horse[No.' + str(horse_no) + '] has exit race')
                                    self.wpTable[horse_no] = info
                                else:
                                    common.log(str(race_date) + str(race_no) + 'horse[No.' + str(horse_no) + '] has added, parse page error')
                            else:
                                common.log(str(race_date) + str(race_no) + 'horse[No.' + str(horse_no) + '] has exit race')
                                info = {}
                                info['exit_race'] = True
                                self.wpTable[horse_no] = info
                    else:
                        pass
        for key, value in self.wpTable.items():
            print('parse page success=>', key, value)

    def __del__(self):
        print('===== spider over ====')

