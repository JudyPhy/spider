from chromeDriver import singleton_chrome
from common import common
import time


class HorseInfoParse(object):

    def __init__(self, url):
        self.horse_info = {}
        self.__initHorseInfo()

        self.horse_seasonInfo = {}

        self.__parse(url)
        pass

    def __initHorseInfo(self):
        self.horse_info['name'] = ''
        self.horse_info['code'] = ''
        pass

    def __parse(self, url):
        try:
            print('request=>', url)
            singleton_chrome.driver.get(url)
            time.sleep(0.1)
            self.__parseHorseInfoPage(url)
        finally:
            pass

    def __parseHorseInfoPage(self, url):
        try:
            ele_name = singleton_chrome.driver.find_element_by_xpath('.//td[@class="subsubheader"]')
            if ele_name:
                name = ele_name.text.replace('&nbsp;','').replace('(Retired)', '')
                if '(' in name:
                    array_name = name.split('(')
                    self.horse_info['name'] = array_name[0].strip()
                    self.horse_info['code'] = array_name[len(array_name) - 1].replace(')', '').strip()
                else:
                    self.horse_info['name'] = name.strip()
                    self.horse_info['code'] = 0
                print('name:', self.horse_info['name'], ' code:', self.horse_info['code'])
            else:
                pass

            table_horse_race = singleton_chrome.driver.find_elements_by_xpath('.//table[@class="bigborder"]')
            if len(table_horse_race) > 0:
                trs = table_horse_race[0].find_elements_by_xpath('.//tr')
                season = ''
                for tr in trs[1:]:
                    if tr.text == '':
                        continue
                    tds = tr.find_elements_by_xpath('./td')
                    if len(tds) == 1:
                        season = tds[0].text.strip()
                        # print('season:', season)
                    elif len(tds) == 19 and season != '':
                        if season not in self.horse_seasonInfo.keys():
                            self.horse_seasonInfo[season] = []
                        dict = {}
                        dict['race_id'] = tds[0].text.strip()
                        dict['pla'] = tds[1].text.strip()
                        dict['race_date'] = tds[2].text.strip()
                        dict['rc_track_course'] = tds[3].text.strip()
                        dict['dist'] = tds[4].text.strip()
                        dict['g'] = tds[5].text.strip()
                        dict['class'] = tds[6].text.strip()
                        dict['dr'] = tds[7].text.strip()
                        dict['rtg'] = tds[8].text.strip()
                        dict['trainer'] = tds[9].text.strip()
                        dict['jockey'] = tds[10].text.strip()
                        dict['lbw'] = tds[11].text.strip()
                        dict['win_odds'] = tds[12].text.strip()
                        dict['act_wt'] = tds[13].text.strip()

                        running_position = tds[14].text.strip()
                        array_rp = running_position.split(' ')
                        str_rp = ''
                        for item_rp in array_rp:
                            p = item_rp.replace(' ', '')
                            if p != '':
                                str_rp += p + '|'
                        if str_rp[len(str_rp) - 1] == '|':
                            str_rp = str_rp[: len(str_rp) - 1]
                        dict['running_position'] = str_rp

                        dict['finish_time'] = tds[15].text.strip()
                        dict['declar_horse_wt'] = tds[16].text.strip()
                        dict['gear'] = tds[17].text.strip()

                        self.horse_seasonInfo[season].append(dict)
                    else:
                        print('table column error')
                # for key, value in self.horse_seasonInfo.items():
                #     # for row in value:
                #     print(key, len(value))
        except Exception as error:
            common.log('chrome page error:' + url + '\n' + str(error))
        pass


